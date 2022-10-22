import email
from email.message import EmailMessage
from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from admin_app.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
import random


def studentPage(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    return render(request,'student_temp/studentPage.html',{'profile':profile})
