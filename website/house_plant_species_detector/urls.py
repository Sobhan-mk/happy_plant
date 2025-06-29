from django.urls import path
from .views import *


app_name = 'house_plant_species_detector'

urlpatterns = [
    path('detector/', house_plant_detector, name='detector'),
    path('about_model/', about_model, name='about_model'),
]

