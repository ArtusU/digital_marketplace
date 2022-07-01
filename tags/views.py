from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Tag
from analytics.models import TagView



class TagDetailView(DetailView):
    model = Tag
    
    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            TagView.objects.add_count(user=self.request.user, tag=self.get_object())
        return context
    

class TagListView(ListView):
    model = Tag
