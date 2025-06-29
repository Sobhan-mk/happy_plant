from django.contrib.auth.forms import forms
from .models import PlantLeaf

#تصویر گیاه آسیب دیده را از کاربر دریافت می کند.
class PlantLeafForm(forms.ModelForm):
    class Meta:
        model = PlantLeaf
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
                'style': 'background-color: #14191e; color: white; border: 1px solid gray; border-radius: 10px;',
                'placeholder' : 'تصویر خود را وارد کنید'
            }),
        }

#مانند فهرست گیاهان خانگی، این فرم نیز برای جستوجو در فهرست بیماری گیاهان ساخته شده است.
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput({'placeholder' : "جستوجو..." ,
                                                                    'style': 'width: 100%; background-color: #262a33; color: white; border: 0.1px solid lightgray; border-radius:10px; height:40px'
                                                                    }))