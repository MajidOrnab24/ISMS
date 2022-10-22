
from dataclasses import field
import email
from wsgiref import validate
from django import forms
from main.models import *
from datetime import date
import datetime
from django.forms.widgets import DateInput
from admin_app.models import *
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.utils.translation import gettext_lazy as _
import re

def validate_emails(value):
    is_valid=validate_email(value,verify=True)
    if  not is_valid:
          raise ValidationError(
            _('%(value)s is not an a valid email'),
            params={'value': value},
          )
def validate_passwords(value):
    if  len(value) < 8:
          raise ValidationError(
            _('Password is too short must have 8 characters'),
            params={'value': value},
          )
    elif not re.findall('[A-Z]', value):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                params={'value': value},
            )
    elif not re.findall('[a-z]', value):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                params={'value': value},
            )
    elif not len(re.findall('\d', value)) >= 1:
            raise ValidationError(
                _("The password must contain at least digit, 0-9."),
                params={'value': value},
            )
        


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
                "class": "form-control",'size': '40'
            }
        ),validators=[validate_emails]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",'size': '40'
            }
        ),validators=[validate_passwords]
    )

    
    class Meta:
        model = Student
        fields = ('email', 'password')

class registerFaculty(forms.ModelForm):
    email = forms.EmailField(widget= forms.TextInput(attrs={"class": "form-control",'size': '40','title': 'Your name'} ),validators=[validate_emails])
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'size': '40' }),validators=[validate_passwords])
    class Meta:
        model = Faculty
        fields = ('email', 'password')

class facultyprofileform(forms.ModelForm):
     date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
     name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     room=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     address=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     department=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=department.objects.all(),empty_label="Select Department")
     education=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     phone=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     image=forms.ImageField(widget=forms. ClearableFileInput(attrs={"class": "form-control",'size': '40' }))
     gender=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=gender_choices)

     class Meta:
        model=FacultyProfile
        fields =('name','room','address','department','education','gender','phone','image','date_of_birth')
     def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")



class profileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
    session = forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
    student_ID=forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control",'size': '40' }))
    father_name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    mother_name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    address=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
    department=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=department.objects.all(),empty_label="Select Department")
    phone=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    image=forms.ImageField(widget=forms. ClearableFileInput(attrs={"class": "form-control",'size': '40' }))
    gender=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=gender_choices)

    class Meta:
        model = StudentProfile
        fields = ('name','student_ID','address','father_name','mother_name','phone','semester','image','gender',
        'date_of_birth' ,'department','session')
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

class updateStudentForm(forms.ModelForm):
    email = forms.EmailField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(widget=forms.PasswordInput( attrs={"class": "form-control"}))
    
    class Meta:
        model = Student
        fields = ('email', 'password')

