from ckeditor.fields import RichTextField
from django.db import models


class RoadMap(models.Model):
    event = models.TextField(max_length=500)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = RichTextField()

class QuestionBank(models.Model):
    year = models.CharField(max_length=50)
    file = models.FileField()
