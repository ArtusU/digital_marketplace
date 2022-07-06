import os
from io import StringIO
from mimetypes import guess_type
from webbrowser import get
from wsgiref.util import FileWrapper
from django.db.models import Q
from django.conf import settings
from django.core.files import File
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .mixins import ProductManagerMixin
from .models import Product
from .forms import ProductModelForm
from analytics.models import TagView
from tags.models import Tag
from digitalmarketplace.mixins import (
    MultipleSlugMixin, 
    SubmitBtnMixin,
    LoginRequiredMixin
)


class ProductListView(ListView):
    model = Product
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|
                        Q(description__icontains=query)
                        ).order_by('title')
            return qs
        return qs
    

class ProductDetailView(MultipleSlugMixin, DetailView):
    model = Product 
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        for tag in tags:
            new_view = TagView.objects.add_count(self.request.user, tag)
        return context
    
    
    
class ProductDownloadView(MultipleSlugMixin, DetailView):
    model = Product
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.myproducts.products.all:
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(StringIO(filepath))
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type=mimetype)
            if not request.GET.get("preview"):
                response["Content-Disposition"] = f"attachment; filename={obj.media.name}"
            response["X-Sendfile"] = obj.media.name
            return response
        else:
            raise Http404
    
    
class ProductCreateView(LoginRequiredMixin, MultipleSlugMixin, SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = 'Add Product'
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        tags = form.cleaned_data.get('tags')
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)
        return valid_data
    
    def get_success_url(self):
        return reverse('products:list')
    

class ProductUpdateView(ProductManagerMixin, MultipleSlugMixin, SubmitBtnMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = 'Update Product'
    
    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial['tags'] = ", ".join([x.title for x in tags])
        return initial
    
    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get('tags')
        obj.tag_set.clear()
        if tags:
            tag_list = tags.split(',')
            obj = self.get_object()
            obj.tag_set.clear()
            for tag in tag_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data
