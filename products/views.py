from itertools import product
from webbrowser import get
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product
from .forms import ProductModelForm



class ProductListView(ListView):
    model = Product
    

class ProductDetailView(DetailView):
    model = Product 
     

def create_view(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create Product"
        }
    return render(request, template, context)


def edit_view(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    print(product)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        #instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
		"object": product,
		"form": form,
		"submit_btn": "Edit Product"
	}
    return render(request, template, context)