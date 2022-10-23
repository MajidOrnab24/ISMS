import email
from email.message import EmailMessage
from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.urls import is_valid_path
from main.models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
import random
from admin_app.models import *



def logError(request):
    return render(request,'logError.html')

          
# Home
def home (request):
    return render(request,'homepage.html' )
def general_login(request):
    return render(request,'general_login.html')


def facultyPage(request):
    return render(request,'facultyPage.html')
def staffLibPage(request):
    return render(request,'staffLibPage.html')
def staffMedPage(request):
    return render(request,'staffMedPage.html')
def logout_request(request):
    logout(request)
    return redirect('general_login')

# Sign in views
def signinStudent(request):
    curr_user=request.user
    if  request.user.is_authenticated:
        if curr_user.is_student:
            return redirect('studentPage')
        elif curr_user.is_admin or curr_user.is_faculty or curr_user.is_staff_lib or curr_user.is_staff_med :
             return redirect('logError')
         
    else:
        form = signinformStudent(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            if UserAccount is not None and not UserAccount.is_student:
                if UserAccount.is_admin:
                   types='Admin'
                else:
                   types=UserAccount.type
                messages.error(request,'Wrong user type Student only. '+types.title()+' type not accepted')
                return redirect('signinStudent')
            elif  UserAccount is not None and UserAccount.is_student:
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('studentPage')
                
            else:
                messages.error(request,'username or password not correct')
                return redirect('signinStudent')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'signinStudent.html', {'form': form})



def signinFaculty(request):
    curr_user=request.user
    if  request.user.is_authenticated:
        if curr_user.is_faculty:
            return redirect('facultyPage')
        elif curr_user.is_admin or curr_user.is_student or curr_user.is_staff_lib or curr_user.is_staff_med :
             return redirect('logError')
         

    else:
        form = signinformFaculty(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            if UserAccount is not None and not UserAccount.is_faculty:
                if UserAccount.is_admin:
                   types='Admin'
                else:
                   types=UserAccount.type
                messages.error(request,'Wrong user type, Faculty only. '+types.title()+' type not accepted')
                return redirect('signinFaculty')
            elif  UserAccount is not None and UserAccount.is_faculty :
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('facultyPage')
                
            else:
                messages.error(request,'username or password not correct')
                return redirect('signinFaculty')
        else:
            messages.error(request,'Error validating form')
    return render(request, 'signinFaculty.html', {'form': form})

def signinStaff(request):
    curr_user=request.user
    if  request.user.is_authenticated:
        if curr_user.is_staff_lib:
            return redirect('staffLibPage')
        elif curr_user.is_staff_med:
            return redirect('staffMedPage')
        elif curr_user.is_admin or curr_user.is_student or curr_user.is_faculty :
             return redirect('logError')
    else:
        form = signinformStaff(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)
            if UserAccount is not None and not UserAccount.is_staff_lib and not UserAccount.is_staff_med:
                if UserAccount.is_admin:
                   types='Admin'
                else:
                   types=UserAccount.type
                messages.error(request,'Wrong user type  Staff only. '+types.title()+' type not accepted')
                return redirect('signinStaff')
            if  UserAccount is not None and UserAccount.is_staff_lib:
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffLibPage')
            if  UserAccount is not None and UserAccount.is_staff_med:
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffMedPage')
                
            else:
                messages.error(request,'username or password not correct')
                return redirect('signinStaff')
        else:
            messages.error(request,'error validating form')
    return render(request, 'signinStaff.html', {'form': form})

    

