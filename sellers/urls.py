from django.urls import path

from .views import SellerDasboard


app_name = 'sellers'

urlpatterns = [
    path('', SellerDasboard.as_view(), name='dashboard')
]
