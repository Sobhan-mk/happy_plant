from django.contrib.auth.urls import path
from . import views

#برای نمیش توضیحات گیاهان، باید ابتدا id آن گیاه از طرف لینک ارجاع دهنده ارسال شود.
app_name = 'PLDdetector'
urlpatterns = [
    path('detector_model/', views.detector_model, name='detector_model'),
    path('plant_diseases_list/', views.plant_diseases_list, name='plant_diseases_list'),
    path('plant_diseased_detail/<int:id>', views.plant_diseased_detail, name='plant_diseased_detail'),
    path('about_model/', views.about_model, name='about_model')
]