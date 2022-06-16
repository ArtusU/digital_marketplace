from itertools import product
from webbrowser import get
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Product
from .forms import ProductModelForm
from digitalmarketplace.mixins import MultipleSlugMixin, SubmitBtnMixin


class ProductListView(ListView):
    model = Product
    

class ProductDetailView(MultipleSlugMixin, DetailView):
    model = Product 
    
    
class ProductCreateView(MultipleSlugMixin, SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/create/"
    submit_btn = 'Add Product'
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        return valid_data
    

class ProductUpdateView(SubmitBtnMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/"
    submit_btn = 'Update Product'
    
    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(ProductUpdateView, self).get_object(*args, **kwargs)
        if obj.user == user or user in obj.managers.all():
            return obj
        else:
            raise Http404
