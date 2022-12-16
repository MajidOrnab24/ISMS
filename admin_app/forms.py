
from dataclasses import field, fields
import email
from pyexpat import model
from turtle import textinput, title
from wsgiref import validate
from django import forms
from django.forms import TextInput
from main.models import *
from admin_app.models import *
from datetime import date
import datetime
from django.forms.widgets import DateInput
from admin_app.models import *
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.utils.translation import gettext_lazy as _
import re
from main.admision_models import *
import DNS
DNS.defaults['server']=['8.8.8.8', '8.8.4.4']

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
        
def validate_file_size(value):
    filesize= value.size
    if filesize > 5*1024*1024:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")



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
     designation=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=designation_choices)
     phone=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     image=forms.ImageField(widget=forms. ClearableFileInput(attrs={"class": "form-control",'size': '40' }))
     gender=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=gender_choices)


     class Meta:
        model=FacultyProfile
        fields =('name','room','address','department','designation','education','gender','phone','image','date_of_birth')
     def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

cr_CHOICES = [
    (False, 'No'),
    (True, 'Yes')

]

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
    semester=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=sem_choices)
    section=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=section_choices)
    CR = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=cr_CHOICES,label='CR')


    class Meta:
        model = StudentProfile
        fields = ('name','student_ID','address','father_name','mother_name','phone','semester','section','image','gender',
        'date_of_birth' ,'department','CR','session')
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")



class changePassByadmin(forms.Form):

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

class registerStaffMed(forms.ModelForm):
    email = forms.EmailField(widget= forms.TextInput(attrs={"class": "form-control",'size': '40','title': 'Your name'} ),validators=[validate_emails])
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'size': '40' }),validators=[validate_passwords])
    class Meta:
        model = StaffMed
        fields = ('email', 'password')

class staff_med_profileform(forms.ModelForm):
     date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
     name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     designation=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     address=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     duty=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     phone=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     image=forms.ImageField(widget=forms. ClearableFileInput(attrs={"class": "form-control",'size': '40' }))
     gender=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=gender_choices)

     class Meta:
        model=StaffMedProfile
        fields =('name','address','designation','gender','phone','image','date_of_birth','duty')
     def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

class registerStaffLib(forms.ModelForm):
    email = forms.EmailField(widget= forms.TextInput(attrs={"class": "form-control",'size': '40','title': 'Your name'} ),validators=[validate_emails])
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'size': '40' }),validators=[validate_passwords])
    class Meta:
        model = StaffLib
        fields = ('email', 'password')

class staff_lib_profileform(forms.ModelForm):
     date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
     name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     designation=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     address=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     duty=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
     phone=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
     image=forms.ImageField(widget=forms. ClearableFileInput(attrs={"class": "form-control",'size': '40' }))
     gender=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=gender_choices)

     class Meta:
        model=StaffLibProfile
        fields =('name','address','designation','gender','phone','image','date_of_birth','duty')
     def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError("Image file too large Please Upload less than 2 mb")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")


class dateInput(forms.DateInput):
    input_type = 'date'
class timeInput(forms.TimeInput):
    input_type = 'time'
class roadMapForm(forms.ModelForm):
    class Meta:
        model = RoadMap
        fields = "__all__"
        widgets = {
            'event': TextInput(attrs={'size': '60',"class": "form-control"}),
            'time': timeInput(),
            'date': dateInput(attrs={'min':datetime.datetime.now().date(),"class": "form-control"}),
        }

class semesterQuestionBankForm(forms.ModelForm):
    year=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    file=forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "form-control",'size': '40' }),validators=[validate_file_size])
    department=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=dept_choices)
    semester=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=semester_choices)
    class Meta:
        model = SemesterQuestionBank
        fields = ('year','department','semester','file')


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

class bookForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    author=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    category=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=category_choices)
    shelf_no= forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    class Meta:
        model = Books
        fields = ('title','author','category','shelf_no')

class StudentbookForm(forms.Form):
    student_ID=forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control",'size': '40' }))
    borrow_date=forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
    due_date=forms.DateField(widget=forms.DateInput(attrs={'type' :'date','min':datetime.datetime.now().date(),"class": "form-control"}))
    book_code=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    
class bookupdateform(forms.ModelForm):
    borrow_date=forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
    due_date=forms.DateField(widget=forms.DateInput(attrs={'type' :'date','min':datetime.datetime.now().date(),"class": "form-control"}))
    class Meta:
        model =Books
        fields=('borrow_date','due_date')

class medlogsForm(forms.ModelForm):
    student_id=forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control",'size': '40' }))
    disease=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    referred_by=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    details=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
    date= forms.DateField(widget=forms.DateInput(attrs={'type' :'date','max':datetime.datetime.now().date(),"class": "form-control"}))
    


    class Meta:
        model=MedLog
        fields =('student_id','disease','referred_by','details','date')

class medlogsUpdateForm(forms.ModelForm):
    disease=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    referred_by=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    details=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'size': '40' }))
    remuneration_date=forms.DateField(widget=forms.DateInput(attrs={'type' :'date',"class": "form-control"}))
    remuneration=forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control",'size': '40' }))
    


    class Meta:
        model=MedLog
        fields =('disease','referred_by','details','remuneration','remuneration_date')

class CoursesForm (forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'size': '40' }))
    semester=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=sem_choices)
    credit=forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control",'size': '40' }))
    faculty=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=FacultyProfile.objects.all(),empty_label="Select Faculty")
    department=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=department.objects.all(),empty_label="Select Department")
    
    class Meta:
        model=Courses
        fields=('name','semester','credit','faculty','department')

class EnrollmentForm(forms.ModelForm):
    result=forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=grade_choices)
    date_finished= forms.DateField(widget=forms.DateInput(attrs={'type' :'date','min':datetime.datetime.now().date(),"class": "form-control"}))

      

    class Meta:
        model=Enrollment
        fields=('result','date_finished')


class NoticeForm(forms.ModelForm):
    course=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=Courses.objects.all(),empty_label="Select Course")
    content=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'style': 'width: 60em;''height: 30em;' }))

    class Meta:
        model=notice
        fields=('course','content')


class CRNoticeForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'style': 'width: 60em;''height: 30em;' }))
    class Meta:
        model=student_notice
        fields=('content',)


class CourseAssignerForm(forms.ModelForm):
    faculty=forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control" }),queryset=FacultyProfile.objects.all(),empty_label="Select Faculty")
    class Meta:
        model=course_assigner
        fields=('faculty',)