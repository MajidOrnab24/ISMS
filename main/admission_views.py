import email
from email.message import EmailMessage
from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
import random


def admission(request):
    return render(request,'admission_temp/admission.html')
def about(request):
    return render(request,'admission_temp/about.html')
def faq(request):
    return render(request,'admission_temp/faq.html')
def questionBank(request):
    return render(request,'admission_temp/questionBank.html')
def roadMap(request):
    return render(request,'admission_temp/roadmap.html')