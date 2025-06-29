from django import forms
from .models import Plants

#برای دریافت ورودی و سرچ در فهرست نام گیاهان خانگی ساخته شده است.
class SearchPlantNames(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput({'placeholder' : "جستوجو..." ,
                                                                    'style': 'width: 100%; background-color: #262a33; color: white; border: 0.1px solid lightgray; border-radius:10px; height:40px'
                                                                    }))

#فرمی است که برای دریافت شرابط نگهداری به صورت فیلد های جداگانه و فیلتر کردن آنها ساخته شده است.
class PlantRecommendation(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ['light', 'temperature', 'water', 'soil_type']#فیلد های نوشته شده را دریافت می کند.
        widgets = {
            'light': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                'placeholder': 'نور'
            }),
            'temperature': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                'placeholder': 'دما'
            }),
            'water': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                'placeholder': 'آب'
            }),
            'soil_type': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                'placeholder': 'نوع خاک'
            })
        }


