import email
from email.policy import default
from enum import unique
from operator import truediv
from pickle import TRUE
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


def filepath(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % (instance.name,instance.student_ID,ext)
    return os.path.join('uploads/', filename)

def filepathFaculty(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % (instance.name,instance.email_id,ext)
    return os.path.join('faculty_images/', filename)
def filepathStaff(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % (instance.name,instance.email_id,ext)
    return os.path.join('staff_images/', filename)

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
sem_choices =[
    (1,"1"),
    (2,"2"),
    (3,"3"),
    (4,"4"),
    (5,"5"),
    (6,"6"),
    (7,"7"),
    (8,"8"),
]
section_choices =[
    (1,"1"),
    (2,"2"),
    (3,"3"),

]
gender_choices = [
    ('MALE',"MALE"),
    ('FEMALE',"FEMALE"),
]

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
    section = models.IntegerField(choices=section_choices, default=1)
    CR=models.BooleanField(default=False)

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
        return self.name


    @receiver(post_save, sender=Student)
    def create_student_profile(sender, instance, created, **kwargs):
     if created:
        StudentProfile.objects.create(email=instance)


designation_choices = [
    ('Lecturer',"Lecturer"),
    ('Assistant Professor',"Assistant Professor"),
    ('Associate Professor',"Associate  Professor"),
    ('Professor',"Professor"),
]
class FacultyProfile(models.Model):
    name = models.CharField(max_length=256)
    email = models.OneToOneField(Faculty, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    room = models.CharField(max_length=256)
    phone =  models.CharField(max_length=15)
    image = models.ImageField(upload_to=filepathFaculty)
    designation=models.CharField(max_length=30,choices=designation_choices,default='Lecturer')
    gender=models.CharField(max_length=30,choices=gender_choices,default='MALE')
    date_of_birth = models.DateField(max_length=10, null =True)
    department = models.ForeignKey(department,on_delete=models.CASCADE,null=True)
    education = models.TextField()
    designation_hier=models.IntegerField(default=1)

    @property
    def email_faculty(self):
        return self.email.email
        
    def __str__(self):
        return self.name
    @receiver(post_save, sender=Faculty)
    def create_faculty_profile(sender, instance, created, **kwargs):
     if created:
        FacultyProfile.objects.create(email=instance)

class DeptHeadFaculty(models.Model):
    dept = models.OneToOneField(department, on_delete=models.CASCADE, primary_key=True)
    email=models.OneToOneField(FacultyProfile, on_delete=models.SET_NULL, null =True,blank =True)

    def __str__(self):
        return self.dept.dept_name
    @property
    def head_name(self):
        return self.email.name
    

class StaffMedProfile(models.Model):
    name = models.CharField(max_length=256)
    email = models.OneToOneField(StaffMed, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    designation = models.CharField(max_length=256)
    phone =  models.CharField(max_length=15)
    date_of_birth = models.DateField(max_length=10, null =True)
    image = models.ImageField(upload_to=filepathStaff)
    gender=models.CharField(max_length=30,choices=gender_choices,default='MALE')
    duty = models.TextField()
    
    @property
    def email_staff_med(self):
        return self.name
        
    def __str__(self):
        return self.name
    @receiver(post_save, sender=StaffMed)
    def create_med_staff_profile(sender, instance, created, **kwargs):
     if created:
        StaffMedProfile.objects.create(email=instance)

class StaffLibProfile(models.Model):
    name = models.CharField(max_length=256)
    email = models.OneToOneField(StaffLib, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    designation = models.CharField(max_length=256)
    phone =  models.CharField(max_length=15)
    date_of_birth = models.DateField(max_length=10, null =True)
    image = models.ImageField(upload_to=filepathStaff)
    gender=models.CharField(max_length=30,choices=gender_choices,default='MALE')
    duty = models.TextField()
    
    @property
    def email_staff_lib(self):
        return self.email.email
        
    def __str__(self):
        return self.name
    @receiver(post_save, sender=StaffLib)
    def create_lib_staff_profile(sender, instance, created, **kwargs):
     if created:
        StaffLibProfile.objects.create(email=instance)
grade_choices =[
    (4.00,"A+"),
    (3.75,"A"),
    (3.50,"A-"),
    (3.25,"B+"),
    (3.00,"B"),
    (2.75,"B-"),
    (2.50,"C+"),
    (2.25,"C"),
    (2.00,"D"),
    (0.00,"F"),
]
class Courses(models.Model):
    name = models.CharField(max_length=128)
    semester=models.IntegerField(null=True)
    credit =models.FloatField(null=True)
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.SET_NULL,null=TRUE,blank=True,)
    students = models.ManyToManyField(StudentProfile, through='Enrollment')
    department = models.ForeignKey(department,on_delete=models.SET_NULL,null=True)
    created_d_ID=models.IntegerField(null=True)
    def __str__(self):
        return self.name
  
class Enrollment(models.Model):
    students = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    result = models.FloatField(choices=grade_choices,null=True,blank=True,default=0.0)
    date_joined = models.DateField(max_length=10, null =True)
    date_finished = models.DateField(max_length=10,null=True,blank=True)
    def __str__(self):
        return self.courses.name

category_choices = [
    ('MATH',"MATH"),
    ('PHYSICS',"PHYSICS"),
    ('CHEMISTRY',"CHEMISTRY"),
    ('HUMANITIES',"HUMANITIES"),
    ('ELECTRICAL',"ELECTRICAL"),
    ('COMPUTER SCIENCE',"COMPUTER SCIENCE"),
    ('MECHANICAL',"MECHANIAL"),
    ('CIVIL',"CIVIL"),
    ('INDUSTRIAL',"INDUSTRIAL"),
    ('BUSINESS',"BUSINESS"),
    ('MAANGEMENT',"MANAGEMENT"),


    
]
class Books(models.Model):
    title=  models.CharField(max_length=256)
    author=  models.CharField(max_length=256)
    book_code=models.CharField(max_length=256)
    shelf_no= models.IntegerField(null=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL,null=True,blank=True)
    category=models.CharField(max_length=30,choices=category_choices,null=True,blank=True,default=None)
    borrow_date= models.DateField(max_length=10, null =True,blank=True)
    due_date= models.DateField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.title
    @property
    def student_borrowed(self):
        return self.stduent.name
    @property
    def is_past_due(self):
     return date.today() > self.due_date

class MedLog(models.Model):
    disease=models.CharField(max_length=256)
    student=models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date= models.DateField(max_length=10, null =True)
    remuneration_date= models.DateField(max_length=10,null=True,blank=True)
    remuneration=models.IntegerField(null=True,blank=True)
    referred_by=models.CharField(max_length=256)
    details= models.TextField()

    def __str__(self):
        return "%s_%s_%s." % (self.student.name, self.disease,self.id)


class notice(models.Model):
   course = models.ForeignKey(Courses, on_delete=models.CASCADE)
   faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE)
   semester=models.IntegerField(default=1)
   content=models.TextField()
   date=models.DateField()
   time= models.TimeField()
   update=models.BooleanField(default=False)
   update_time=models.TimeField(null=True,blank=True)
   update_date=models.DateField(null=True,blank=True)

   def __str__(self):
        return "%s_%s_%s." % (self.course.name,self.faculty.name ,datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
   
class student_notice(models.Model):
   student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
   department=models.ForeignKey(department,on_delete=models.SET_NULL,null=True)
   content=models.TextField()
   semester=models.IntegerField()
   section=models.IntegerField()
   date=models.DateField()
   time= models.TimeField()
   update=models.BooleanField(default=False)
   update_time=models.TimeField(null=True,blank=True)
   update_date=models.DateField(null=True,blank=True)

   def __str__(self):
        return "%s_%s_%s." % (self.student.name,self.department.dept_name ,datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    
    

class course_assigner(models.Model):
    faculty=models.ForeignKey(FacultyProfile,on_delete=models.CASCADE)
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    def __str__(self):
        return "%s_%s" % (self.faculty.name,self.department.dept_name )