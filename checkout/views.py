import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.shortcuts import render


class CheckoutTestView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # raise Http404
            data = {
                "works": True,
                "time": datetime.datetime.now(),
            }
            return JsonResponse(data)
        return HttpResponse('Hello there!')
    
    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/test.html', context={})

