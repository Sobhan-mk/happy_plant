from django import forms
from .models import User, Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField as ROPHF


# این فرم برای ساخت کاربر جدید در admin panel نمایش داده می شود
class UserCreateForm(forms.ModelForm):
    pass_1 = forms.CharField(widget=forms.PasswordInput)
    pass_2 = forms.CharField(widget=forms.PasswordInput)

    #این فرم از form.ModelForm ارث بری میکند. بعنی برای پر کردن و دریافت فیلدهای یک مدل مشخص ساخته شده است. این مدل در class Meta و فیلد هایش در fields تعریف می شوند.
    class Meta:
        model = User
        fields = ['username', 'email']

    #مساوی بودن و وجود داشتن رمز عبور و تکرار رمز عبور را بررسی می کند.
    def clean_pass_2(self):
        data = self.cleaned_data
        if data["pass_1"] and data["pass_2"] and data["pass_1"] != data["pass_2"]:
            raise forms.ValidationError('passwords dont match')
        return data["pass_2"]

    #حساب کاربری را ذخیره می کند.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set(self.cleaned_data['pass_2'])
        if commit:
            user.save(using=self._db)

        return user
    
#برای دغییر رمز عبور در admin panel ساخته شده است.
class UserChangeForm(forms.ModelForm):
    password = ROPHF

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        return self.initial['password']


#هنگام ساخت کاربر جدید در سایت این فرم نشان داده میشود.
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
                                                                            'style': 'width: 100%; color: black; border: 0.1px solid gray; border-radius: 10px; height: 40px;',
                                                                            }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                                           'style': 'width: 100%; color: black; border: 0.1px solid gray; border-radius: 10px; height: 40px;',
                                                           }), initial='')

    def __init__(self, *args, **kwargs):
        email_initial = kwargs.pop('email_initial', None)
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        if email_initial:
            self.fields['email'].initial = email_initial

    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'style': 'width: 100%;  color: black; border: 0.1px solid gray; border-radius: 10px; height: 40px;',
    }))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                   'style': 'width: 100%; color: black; border: 0.1px solid gray; border-radius: 10px; height: 40px;',
                                                                   }))

#هنگام ورود یک کاربر این فرم نمابش داده می شود.
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 300px; background-color: rgb(37,41,44); color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                                                             }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: 300px; background-color: rgb(37,41,44); color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                                                                 }))


#برای به روز رسانی اطلاعات کاربری یک کاربر، این فرم در صفحه پروفایل نمایش داده می شود.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
                    'username': forms.TextInput(attrs={
                        'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                    }),
                    'email': forms.TextInput(attrs={
                        'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                    }),

                }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


#برای تغییر رمز عبور از این فرم استفاده می شود.
class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs = {'place_holder' : 'رمز عبور قدیمی',
                                                                       'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                                                                       }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'place_holder': 'رمز عبور جدید',
                                                              'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;'}
    ))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs = {'place_holder' : 'تکرار رمز عبور جدید',
                                                                          'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
                                                                          }))