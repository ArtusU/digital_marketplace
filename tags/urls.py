from django.urls import path

from .views import (
    TagDetailView,
    TagListView
    )


app_name = 'tags'

urlpatterns = [
    path('', TagListView.as_view(), name='list'),
    path('<str:slug>/', TagDetailView.as_view(), name='detail'),
]
