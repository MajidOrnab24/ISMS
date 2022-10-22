import email
from email.policy import default
from enum import unique
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import date
import datetime
import os
from main.models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.
# Create your models here.
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)
def filepathFaculty(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('faculty_images/', filename)

CSE = "CSE"
SWE = "SWE"
EEE = "EEE"
ME = "MCE"
IPE = "IPE"
CEE ="CEE"
BTM ="BTM"

dept_choices = (
    (CSE, "CSE"),
    (EEE, "EEE"),
    (SWE, "SWE"),
    (ME, "ME"),
    (IPE, "IPE"),
    (CEE,"CEE"),
    (BTM,"BTM"),
)
class department(models.Model):
    dept_id = models.AutoField(primary_key = True)
    dept_name = models.CharField(max_length=30,choices=dept_choices)
    def __str__(self):
        return self.dept_name
sem_choices ={
    (1,"1"),
    (2,"2"),
    (3,"3"),
    (4,"4"),
    (5,"5"),
    (6,"6"),
    (7,"7"),
    (8,"8"),
}
gender_choices = {
    ('MALE',"MALE"),
    ('FEMALE',"FEMALE"),
}

class StudentProfile(models.Model):

    name = models.CharField(max_length=256)
    email = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    student_ID = models.IntegerField(unique = True,null=True)
    address = models.TextField()
    father_name = models.CharField(max_length=256)
    mother_name = models.CharField(max_length=256)
    phone =  models.CharField(max_length=15)
    semester =models.IntegerField(choices=sem_choices, default=1)
    image = models.ImageField(upload_to=filepath)
    gender=models.CharField(max_length=30,choices=gender_choices,default='MALE')
    date_of_birth = models.DateField(max_length=10, null =True)
    department = models.ForeignKey(department,on_delete=models.SET_NULL,null=True)
    session =  models.DateField(max_length=10, null=True)

    @property
    def age(self):
        return date.today().year - self.date_of_birth.year
    @property
    def session_year(self):
        return self.session.year
    @property
    def email_student(self):
        return self.email.email
        
    def __str__(self):
        return self.email.email


    @receiver(post_save, sender=Student)
    def create_student_profile(sender, instance, created, **kwargs):
     if created:
        StudentProfile.objects.create(email=instance)

class FacultyProfile(models.Model):
    name = models.CharField(max_length=256)
    email = models.OneToOneField(Faculty, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    room = models.CharField(max_length=256)
    phone =  models.CharField(max_length=15)
    image = models.ImageField(upload_to=filepathFaculty)
    gender=models.CharField(max_length=30,choices=gender_choices,default='MALE')
    date_of_birth = models.DateField(max_length=10, null =True)
    department = models.ForeignKey(department,on_delete=models.CASCADE,null=True)
    education = models.TextField()

    @property
    def email_faculty(self):
        return self.email.email
        
    def __str__(self):
        return self.email.email
    @receiver(post_save, sender=Faculty)
    def create_faculty_profile(sender, instance, created, **kwargs):
     if created:
        FacultyProfile.objects.create(email=instance)

class DeptHeadFaculty(models.Model):
    dept = models.OneToOneField(department, on_delete=models.CASCADE, primary_key=True)
    email=models.OneToOneField(FacultyProfile, on_delete=models.SET_NULL, null =True)

    def __str__(self):
        return self.email.email.email
    @property
    def head_name(self):
        return self.email.name
    

