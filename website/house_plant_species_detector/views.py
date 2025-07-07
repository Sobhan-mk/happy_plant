from django.shortcuts import render, get_object_or_404
from .forms import HouseImageForm
from accounts.models import Profile
from .models import CustomEnsembleModel
from torchvision import transforms
import os
import torch
from PIL import Image
from my_plants.models import Plants

class_lookup_dictionary = {
    0: 81, 1: 90, 2: 12,
    3: 46, 4: 91, 5: 20, 6: 58, 7: 8,
    8: 2, 9: 55, 10: 40, 11: 92,
    12: 66, 13: 93, 14: 83, 15: 94,
    16: 69, 17: 73, 18: 95, 19: 30,
    20: 96, 21: 59, 22: 4, 23: 65,
    24: 97, 25: 98, 26: 99, 27: 68,
    28: 19, 29: 100, 30: 60, 31: 72,
    32: 67, 33: 16, 34: 31, 35: 29,
    36: 6, 37: 76, 38: 28, 39: 10,
    40: 101, 41: 89, 42: 56, 43: 34,
    44: 102, 45: 13, 46: 103
}



model = CustomEnsembleModel()
state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
model.load_state_dict(state_dict)

model.eval()


def house_plant_detector(request):
    image_url = None
    plant = None
    plant_id = None
    model_path = os.path.join(os.getcwd(), 'house_plant_species_detector', 'house_plant_species_detector.pth')

    if request.method == 'POST':
        form = HouseImageForm(request.POST, request.FILES)

        model = CustomEnsembleModel()
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        model.load_state_dict(state_dict)

        model.eval()

        if form.is_valid():
            image = form.cleaned_data['image']
            img = Image.open(image).convert('RGB')
            image_url = form.save().image.url

            HEIGHT, WIDTH = 224, 224
            preprocess = transforms.Compose([
                transforms.RandomRotation(30),
                transforms.Resize((HEIGHT, WIDTH)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomVerticalFlip(p=0.5),
                transforms.RandomCrop((HEIGHT, WIDTH), padding=4),
                transforms.ToTensor(),
            ])
            print('4')
            img = preprocess(img)
            input_batch = img.unsqueeze(0)
            print('4')
            with torch.no_grad():
                output = model(input_batch)
                _, prediction = torch.max(output, 1)

                plant_id = class_lookup_dictionary[prediction.item()]

                plant = get_object_or_404(Plants, id=plant_id)
                print('5')

    else:
        form = HouseImageForm()

    profile = Profile.objects.get(user_id=request.user.id)
    user_plants = profile.users_plants.all()

    context = {
        'form': form,
        'image_url': image_url,
        'user_plants' : user_plants,
        'plant' : plant,
        'plant_id' : plant_id
    }

    return render(request, 'house_plant_species_detector/detector.html', context)


def about_model(request):
    return render(request, 'house_plant_species_detector/about model.html')