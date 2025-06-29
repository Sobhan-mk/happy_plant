import torch
from django.shortcuts import render
from .forms import PlantLeafForm
from PIL import Image
import torchvision.models as models
from torchvision import transforms
import random
import os
from .models import PlantDiseases
from.forms import SearchForm
from django.db.models import Q
import torch.nn as nn


#در این دیکشنری 3 نوع مقدار وجود دارد :
#اگر مفدار str باشد، نشاندهنده گیاه سالم است
#اگر مقدار در قالب int باشد، نشان دهنده گیاه آسیب دیده است و بیان کننده پروفایل بیماری گیاه است.
#برخی از str ها نام بیان کننده آسیب دیدگی یک نوع گیاه هستند. در این صورت تمامی بیماری های وجود برای آن گیاه در دیتا بیس نشان داده می شود.

class_lookup_dictionary = {0: 21,
 1: 'گیاه شما یک سیب سالم است',
 2: 'گیاه شما یک شاهتوت سالم است',
 3: 30,
 4: 'گیاه شما یک سویای سالم است',
 5: 23,
 6: 17,
 7: 32,
 8: 8,
 9: 15,
 10: 14,
 11: 'گیاه شما یک گندم سالم است',
 12: 'گیاه شما یک فلفل دلمه ای سالم است',
 13: 12,
 14: 17,
 15: 22,
 16: 55,
 17: 19,
 18: 33,
 19: 13,
 20: 'گیاه شما یک ذرت سالم است',
 21: 24,
 22: 'گیاه شما یک توت فرنگی سالم است',
 23: 16,
 24: 'گیاه شما یک انگور سالم است',
 25: 35,
 26: 20,
 27: 31,
 28: 39,
 29: 29,
 30: 'گیاه شما یک تمشک سالم است',
 31: 'گیاه شما یک گیلاس سالم است',
 32: 27,
 33: 11,
 34: 18,
 35: 6,
 36: 'گیاه شما یک گوجه سالم است',
 37: 9,
 38: 28,
 39: 34,
 40: 37,
 41: 'گیاه شما یک هلو سالم است',
 42: 10,
 43: 'گیاه شما یک سیب زمینی سالم است'}


def detector_model(request):
    prediction = ''
    image_url = ''
    diseased_plant = None
    str_detection = None

    if request.method == 'POST':
        form = PlantLeafForm(request.POST, request.FILES)

        model_path = os.path.join(os.getcwd(), 'PLDdetector', 'plant_deseases_detector.pth')
        model = models.resnet18(pretrained=True)
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(model.fc.in_features, len(class_lookup_dictionary)))

        model.to('cpu')

        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        model.load_state_dict(state_dict)

        if form.is_valid():
            img = form.cleaned_data['image']
            img = Image.open(img).convert('RGB')
            image_url = form.save().image.url

            HEIGHT, WIDTH = 128, 128

            preprocess = transforms.Compose([
                transforms.RandomRotation(30),
                transforms.Resize((HEIGHT, WIDTH)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomVerticalFlip(p=0.5),
                transforms.RandomCrop((HEIGHT, WIDTH), padding=4),
                transforms.ToTensor(),
            ])

            img = preprocess(img)
            input_batch = img.unsqueeze(0)

            model.eval()

            with torch.no_grad():
                output = model(input_batch)
                _, prediction = torch.max(output, 1)

            detection = class_lookup_dictionary[prediction.item()]
            if isinstance(detection, str):
                str_detection = detection
            else:
                diseased_plant = PlantDiseases.objects.get(id=detection)

    else:
         form = PlantLeafForm()

    random_indexes = [random.randint(0, 37) for _ in range(10)]
    example_files_path = 'C:/Users/sobha/Desktop/django-ai/website/static/pld_example_images'
    example_images = [os.path.join('pld_example_images', os.listdir(example_files_path)[i]) for i in random_indexes]

    context = {
        'form': form,
        'prediction': prediction,
        'image_url': image_url,
        'random_samples': example_images,
        'diseased_plant': diseased_plant,
        'str_detection' : str_detection

    }

    return render(request, 'PLDdetector/detector_model.html', context)


#کاملا مشابه فهرست گیاهان خانگی است.
def plant_diseases_list(request):
    plant_diseases = PlantDiseases.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if 'search' in request.POST:
            if form.is_valid():
                query = form.cleaned_data['query']

                plant_diseases = PlantDiseases.objects.filter(
                    Q(common_name__icontains=query) |
                    Q(persian_name__icontains=query) |
                    Q(scientific_name__icontains=query)
                )
    else:
        form = SearchForm()

    context = {
        'plant_diseases' : plant_diseases,
        'form' : form
    }

    return render(request, 'PLDdetector/plant_diseases_list.html', context)

#کاملا مشابه توضیحات گیاهان خانگی است.
def plant_diseased_detail(request, id):
    plant = PlantDiseases.objects.get(id=id)
    refrense = plant.get_refrence()

    context = {'plant' : plant,
               'refrence' : refrense}

    return render(request, 'PLDdetector/plant_diseased_detail.html', context)


def about_model(request):
    return render(request, 'PLDdetector/about model.html')