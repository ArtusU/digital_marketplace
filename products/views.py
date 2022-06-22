import os
from io import StringIO
from mimetypes import guess_type
from webbrowser import get
from wsgiref.util import FileWrapper
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
from digitalmarketplace.mixins import (
    MultipleSlugMixin, 
    SubmitBtnMixin,
    LoginRequiredMixin
)


class ProductListView(ListView):
    model = Product
    

class ProductDetailView(MultipleSlugMixin, DetailView):
    model = Product 
    
    
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
        return valid_data
    
    def get_success_url(self):
        return reverse('products:list')
    

class ProductUpdateView(ProductManagerMixin, MultipleSlugMixin, SubmitBtnMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = 'Update Product'
