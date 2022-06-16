from itertools import product
from webbrowser import get
from django.http import Http404
from django.shortcuts import render, get_object_or_404
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
    
    
class ProductCreateView(LoginRequiredMixin, MultipleSlugMixin, SubmitBtnMixin, CreateView):
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
    

class ProductUpdateView(ProductManagerMixin, MultipleSlugMixin, SubmitBtnMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    success_url = "/products/"
    submit_btn = 'Update Product'
