from django.contrib import admin
from django.urls import path

from products.views import create_view, edit_view, ProductListView, ProductDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', ProductListView.as_view(), name='product_list_view'),
    path('detail/<str:slug>/', ProductDetailView.as_view(), name='product_detail_view'),
    path('detail/<str:slug>/edit/', edit_view, name='edit_view'),
    path('create/', create_view, name='create_view'),
]
