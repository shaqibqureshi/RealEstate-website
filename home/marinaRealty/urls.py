

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_legacy'),
    path('about/',views.about,name='about'),
   path('properties/', views.property_list, name='properties'),
  
    # Matches {% url 'property_detail' property.pk %} in properties.html
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    
    path('contact/',views.contact,name='contact'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
]
