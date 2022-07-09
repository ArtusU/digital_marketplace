import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.shortcuts import render


#@method_decorator(csrf_exempt, name='dispatch')
class CheckoutTestView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # raise Http404
            data = {
                "works": True,
                "time": datetime.datetime.now(),
            }
            return JsonResponse(data)
        return HttpResponse('Hello there!')
    
    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/test.html', context={})

