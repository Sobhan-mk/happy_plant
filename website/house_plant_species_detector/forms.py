from django import forms
from .models import HousePlantImages

#برای دریافت تصویری از کاربر این فرم را نمایش می دهیم.
class HouseImageForm(forms.ModelForm):
    class Meta:
        model = HousePlantImages
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
                'style': 'background-color: #14191e; color: white; border: 1px solid gray; border-radius: 10px;',
                'placeholder' : 'تصویر خود را وارد کنید'
            }),
        }
        labels = {'image': ''}
