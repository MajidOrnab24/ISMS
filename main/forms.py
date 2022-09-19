
# import form class from django
from django import forms
from main.models import *
  
  
# create a ModelForm
class signinform(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    # class Meta:
    #     model = Student
    #     fields = ('email', 'password')