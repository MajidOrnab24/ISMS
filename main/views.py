import email
from email.message import EmailMessage
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

# Create your views here.


def home (request):
    return render(request,'homepage.html' )
def general_login(request):
    return render(request,'general_login.html')
def admission(request):
    return render(request,'admission.html')
def signup(request):
    return render(request,'signup.html')
def signout(request):
    return render(request,'signout.html')
# student page views
def studentPage(request):
    return render(request,'studentPage.html')
def facultyPage(request):
    return render(request,'facultyPage.html')
def staffLibPage(request):
    return render(request,'staffLibPage.html')
def staffMedPage(request):
    return render(request,'staffMedPage.html')
def logout_request(request):
    logout(request)
    return redirect('general_login')
    

def signinStudent(request):
    form = signinformStudent(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            print( UserAccount)
            if  UserAccount is not None :
                # print("lol")
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('studentPage')
                
            else:
                msg= 'invalid credentials'
                return redirect('signinStudent')
        else:
            msg = 'error validating form'
    return render(request, 'signinStudent.html', {'form': form, 'msg': msg})

def signinFaculty(request):
    form = signinformFaculty(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            print( UserAccount)
            if  UserAccount is not None :
                # print("lol")
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('facultyPage')
                
            else:
                msg= 'invalid credentials'
                return redirect('signinFaculty')
        else:
            msg = 'error validating form'
    return render(request, 'signinFaculty.html', {'form': form, 'msg': msg})
def signinStaffLib(request):
    form = signinformStaffLib(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            print( UserAccount)
            if  UserAccount is not None :
                # print("lol")
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffLibPage')
                
            else:
                msg= 'invalid credentials'
                return redirect('signinStaffLib')
        else:
            msg = 'error validating form'
    return render(request, 'signinStaffLib.html', {'form': form, 'msg': msg})
def signinStaffMed(request):
    form = signinformStudent(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            print( UserAccount)
            if  UserAccount is not None :
                # print("lol")
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffMedPage')
                
            else:
                msg= 'invalid credentials'
                return redirect('signinStaffMed')
        else:
            msg = 'error validating form'
    return render(request, 'signinStaffMed.html', {'form': form, 'msg': msg})
    
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     user = auth.authenticate(email=email, password=password)

    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect('/')
    #     else:
    #         messages.info(request, 'Credentials Invalid')
    #         return redirect('signin')

    # else:
    #     return render(request, 'signin.html')


