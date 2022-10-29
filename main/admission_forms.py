from django import forms
from main.admision_models import *
from dataclasses import field
import email
from turtle import textinput
from wsgiref import validate
from django import forms
from django.forms import TextInput
from main.models import *
from datetime import date
import datetime
from django.forms.widgets import DateInput
from admin_app.models import *
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.utils.translation import gettext_lazy as _
import re
from main.admision_models import *
from admin_app.forms import validate_file_size


class dateInput(forms.DateInput):
    input_type = 'date'
class timeInput(forms.TimeInput):
    input_type = 'time'
class roadMapForm(forms.ModelForm):
    class Meta:
        model = RoadMap
        fields = "__all__"
        widgets = {
            'time': timeInput(),
            'date': dateInput(),
        }

class questionBankForm(forms.ModelForm):
    file=forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "form-control",'size': '40' }),validators=[validate_file_size])
    year=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    class Meta:
        model = QuestionBank
        fields = "__all__"


class faqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = "__all__"
        widgets = {
            'question': forms.TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
        }



