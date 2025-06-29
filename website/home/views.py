import random

from django.shortcuts import render
from .forms import UserHomeRegisterForm
from my_plants.models import Plants
from PLDdetector.models import PlantDiseases


def home(request):
    email = None
    if request.user.is_authenticated:
        pld_detector_url = 'PLDdetector:detector_model'
    else:
        pld_detector_url = 'accounts:login'

    if request.method == 'POST':
        form = UserHomeRegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
    else:
        form = UserHomeRegisterForm()

    plant_ids = list(Plants.objects.values_list('id', flat=True))
    random.shuffle(plant_ids)
    random_plant_ids = plant_ids[:5]
    random_plants = Plants.objects.filter(id__in=random_plant_ids)

    diseased_plant_ids = list(PlantDiseases.objects.values_list('id', flat=True))
    random.shuffle(diseased_plant_ids)
    random_diseased_plant_ids = plant_ids[:5]
    random_diseased_plant = PlantDiseases.objects.filter(id__in=random_diseased_plant_ids)

    context = {
        'form': form,
        'email': email,
        'pld_detector_url': pld_detector_url,
        'random_plants': random_plants,
        'random_diseased_plant' : random_diseased_plant
    }

    return render(request, 'home/home.html', context)

