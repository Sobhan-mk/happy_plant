from django.db import models
import torch
import torch.nn as nn
from torch.nn import Conv2d, BatchNorm2d, ReLU, Dropout, AdaptiveAvgPool2d, MaxPool2d
import torchvision.models as torch_models
from efficientnet_pytorch import EfficientNet
from torch.nn import Module

#مدلی است که تصاویری را ذخیره سازی می کند. اما مربوط به کاربر خاصی نمی باشد
class HousePlantImages(models.Model):
    image = models.ImageField(upload_to='house_plant_images')

    def __str__(self):
        return self.image.name

#این کلاس ساختار مدل pytorch را تعریف می کند که برای لود کردن با استفاده از مدل ذخیره شده به صورت dtate_dict ضروری است.
#اطلاعات بیشنر در مورد این مدل را در فایل آموزش مدل تشخیص گونه گیاهان خانگی مشاهده کنید.
class CustomEnsembleModel(Module):
  def __init__(self, num_classes = 47):
    super(CustomEnsembleModel, self).__init__()
    self.resnet50 = torch_models.resnet50(pretrained=True)
    self.efficient_net =   EfficientNet.from_pretrained('efficientnet-b0')

    self.resnet50 = nn.Sequential(*list(self.resnet50.children())[:-2])

    self.custom_resnet = nn.Sequential(
        Conv2d(2048, 1024, kernel_size=3, stride=1, padding=1, bias=False),
        BatchNorm2d(1024),
        ReLU(inplace=True),
        Dropout(p=0.5),
        MaxPool2d(kernel_size=3, stride=2),

        Conv2d(1024, 512, kernel_size=3, stride=1, padding=1, bias=False),
        BatchNorm2d(512),
        ReLU(inplace=True),
        Dropout(p=0.5),
        nn.AdaptiveAvgPool2d((1, 1))
    )

    self.custom_effnet = nn.Sequential(
            Conv2d(1280, 1024, kernel_size=3, stride=1, padding=1, bias=False),
            BatchNorm2d(1024),
            ReLU(inplace=True),
            Dropout(p=0.5),
            MaxPool2d(kernel_size=3, stride=2),

            Conv2d(1024, 512, kernel_size=3, stride=1, padding=1, bias=False),
            BatchNorm2d(512),
            ReLU(inplace=True),
            Dropout(p=0.5),
            AdaptiveAvgPool2d((1, 1))
      )

    self.fc = nn.Linear(512, num_classes)

  def forward(self, x):
     x1 = self.resnet50(x)
     x1 = self.custom_resnet(x1)
     x1 = torch.flatten(x1, 1)
     x1 = self.fc(x1)

     x2 = self.efficient_net.extract_features(x)
     x2 = self.custom_effnet(x2)
     x2 = torch.flatten(x2, 1)
     x2 = self.fc(x2)

     return (x1 + x2) / 2