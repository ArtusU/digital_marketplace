from django.urls import path

from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView


app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('detail/<str:slug>/', ProductDetailView.as_view(), name='detail'),
    path('detail/<str:slug>/update/', ProductUpdateView.as_view(), name='update'),
]
