from django.shortcuts import get_object_or_404


class SubmitBtnMixin(object):
    submit_btn = None
    
    def get_context_data(self, **kwargs):
        context = super(SubmitBtnMixin, self).get_context_data(**kwargs)
        context['submit_btn'] = self.submit_btn
        return context
    

class MultipleSlugMixin(object):
    model = None
    
    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        ModelClass = self.model
        if slug is not None:
            try:
                obj = get_object_or_404(ModelClass, slug=slug)
            except ModelClass.MultipleObjectsReturned:
                obj = ModelClass.objects.filter(slug=slug).order_by('title').first()
        else:
            obj = super(MultipleSlugMixin, self).get_object(*args, **kwargs)
        return obj
    
    