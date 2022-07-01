from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from dashboard.views import DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', DashboardView.as_view(), name='dashboard'),
    path('products/', include('products.urls', namespace='products')),
    path('tags/', include('tags.urls', namespace='tags')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
