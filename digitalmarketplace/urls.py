from django.contrib import admin
from django.urls import path

from products.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('products/', ProductListView.as_view(), name='product_list_view'),
    path('products/create/', ProductCreateView.as_view(), name='product_create_view'),
    path('products/detail/<str:slug>/', ProductDetailView.as_view(), name='product_detail_view'),
    path('products/detail/<str:slug>/update/', ProductUpdateView.as_view(), name='product_update_view'),
]
