from dataclasses import field
import email
from django import forms
from main.models import *
from admin_app.models import *

# create a form form
class signinformAdmin(forms.Form):
    email = forms.CharField(
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
    
    class Meta:
        model = UserAccount
        fields = ('email', 'password')

class registerStudent(forms.ModelForm):
    email = forms.EmailField(
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

    
    class Meta:
        model = Student
        fields = ('email', 'password')


class profileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ('name','student_ID','address','father_name','mother_name','phone','semester','image','gender','date_of_birth' ,'department','session')

class updateStudentForm(forms.ModelForm):
    # email = forms.EmailField(
    #     widget= forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    
    class Meta:
        model = Student
        fields = ('email', 'password')
