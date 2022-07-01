from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Tag
from analytics.models import TagView



class TagDetailView(DetailView):
    model = Tag
    
    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            analytic_obj, created = TagView.objects.get_or_create(
                                        user=self.request.user, 
                                        tag=self.get_object()
                                        )
            analytic_obj.count += 1
            analytic_obj.save()
        return context
    

class TagListView(ListView):
    model = Tag
