from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Tag



class TagDetailView(DetailView):
    model = Tag
    

class TagListView(ListView):
    model = Tag
