from django.urls import path
from . import views

urlpatterns = [
    path('face/', views.face),
    path('text/', views.text),
    # path('login/', views.login),
]
