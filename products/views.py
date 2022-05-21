from itertools import product
from django.shortcuts import render
from .models import Product


def detail_view(request):
    product = Product.objects.all().first()
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