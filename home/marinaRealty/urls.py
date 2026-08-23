

from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('properties/',views.properties,name='properties'),
    path('contact/',views.contact,name='contact'),
]
