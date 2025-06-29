from django import forms


class UserHomeRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'style': 'width: 400px; color: black; border: 1px solid gray; border-radius: 10px; height: 50px; background-color: white',
    }))