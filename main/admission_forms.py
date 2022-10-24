from django import forms
from main.admision_models import *


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



