from django.shortcuts import render
from django.views.generic import View


class SellerDasboard(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sellers/dashboard.html', {})
