from ckeditor.fields import RichTextField
from django.db import models
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

def path_admissionQ(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('Admission question of ',instance.year,ext)
    return os.path.join('admission_questions/', filename)


class RoadMap(models.Model):
    event = models.TextField(max_length=500)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = RichTextField()

class QuestionBank(models.Model):
    year = models.CharField(max_length=50)
    file = models.FileField(upload_to=path_admissionQ)
