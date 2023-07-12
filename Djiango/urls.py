
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('interface/', include('interface.urls')),
    path('admin/', admin.site.urls),
]
