from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('products.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
