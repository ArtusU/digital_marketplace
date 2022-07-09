import datetime
import json

from django.http import HttpResponse, JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.shortcuts import render

from products.models import Product, MyProducts



class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productID = data['productId']
        print(productID)
        existst = Product.objects.filter(id=productID).exists()
        if not existst:
            raise JsonResponse('Product does not exist', status=404)
        try:
            product_obj = Product.objects.get(id=productID)
        except:
            product_obj = Product.objects.filter(id=productID).first()
        my_products = MyProducts.objects.get_or_create(user=request.user)[0]
        my_products.products.add(product_obj)
        
        return JsonResponse('Item proceed to checkout.', safe=False)


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

