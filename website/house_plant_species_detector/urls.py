from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'house_plant_species_detector'

urlpatterns = [
    path('detector/', house_plant_detector, name='detector'),
    path('about_model/', about_model, name='about_model'),
]


if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
