
# import form class from django
import email
from django import forms
from main.models import *
from admin_app.forms import validate_passwords
from admin_app.forms import ValidationError
from admin_app.forms import validate







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
  
  
# create a Form Student
class signinformStudent(forms.Form):
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
        model = Student
        fields = ('email', 'password')

# Faculty Form

class signinformFaculty(forms.Form):
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
        model = Faculty
        fields = ('email', 'password')


class signinformStaff(forms.Form):
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

class changePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ),validators=[validate_passwords]
    )
    new_password_again = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ),validators=[validate_passwords]
    )