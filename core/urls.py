from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('quality/', views.quality, name='quality'),
    path('contact/', views.contact, name='contact'),
]
