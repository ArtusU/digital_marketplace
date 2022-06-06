from django.contrib import admin
from django.urls import path

from products.views import detail_view, list_view, create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/<str:slug>/', detail_view, name='detail_view'),
    path('create/', create_view, name='create_view'),
    path('', list_view, name='list_view'),
]
