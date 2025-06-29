from django import forms
from .models import Question, Answer

#پرسش سوال
class AskingQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'detail', 'topic']

        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
            }),
            'detail': forms.Textarea(attrs={
                'style': 'width: 100%; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 200px; resize: vertical;',
                'maxlength' : "1000",
            }),
            'topic': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
            })
        }

#تغییر سوال
class QuestionEdit(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'detail', 'topic']

        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
            }),
            'detail': forms.Textarea(attrs={
                'style': 'width: 100%; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 200px; resize: vertical;',
            }),
            'topic': forms.Select(attrs={
                'style': 'width: 300px; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',
            })
        }

#ثبت پاسخ
class SaveAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['detail']

        widgets = {
                    'detail': forms.TextInput(attrs={
                        'style': 'width: 100%; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 200px; resize: vertical;',
                    })}

#جستوجو در سوالات
class SearchQuestions(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput({'placeholder' : "جستوجو",
                                                                    'style': 'width: 100%; background-color: #14191e; color: white; border: 0.1px solid gray; border-radius: 10px; height: 35px;',

                                                                    }))
