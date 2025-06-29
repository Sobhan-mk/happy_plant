from django.contrib.auth.forms import forms
from .models import Approach


class SendApproach(forms.ModelForm):
    class Meta:
        model = Approach
        fields = ['title', 'detail']

        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
            }),
            'detail': forms.Textarea(attrs={
                'style': 'width: 100%; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 200px; resize: vertical;',
            }),
        }
