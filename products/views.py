from itertools import product
from webbrowser import get
from django.shortcuts import render, get_object_or_404
from .models import Product


def detail_view(request, slug):
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
		
	template = 'detail_view.html'
	context = {"object": product}
	return render(request, template, context)


def list_view(request):
	queryset = Product.objects.all()
	template = "list_view.html"
	context = {
		"queryset": queryset
	}
	return render(request, template, context)