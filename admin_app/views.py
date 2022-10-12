import email
from email.message import EmailMessage
from pickle import TRUE
import profile
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
from admin_app.forms import *
import random

# Admin views here.
def adminHome(request):
    return render(request,'admin_temp/adminHome.html')
def adminStudent(request):
    return render(request,'admin_temp/adminStudent.html')
def adminLogin(request):
    curr_user=request.user
    if  request.user.is_authenticated:
        if curr_user.is_admin:
            return redirect('adminHome')
        elif curr_user.is_student or curr_user.is_faculty or curr_user.is_staff_lib or curr_user.is_staff_med :
             return redirect('logError')      

    else:
     form = signinformAdmin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = auth.authenticate(email=email, password=password)

            # print( UserAccount)
            if UserAccount is not None and not UserAccount.is_admin:
                if UserAccount.is_admin:
                   types='Admin'
                else:
                   types=UserAccount.type
                messages.error(request,'Wrong user type, Admin only. '+types.title()+' type not accepted')
                return redirect('admin/login/')

            elif UserAccount is not None and  UserAccount.is_admin:
                # print(UserAccount.type)
                  login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                  return redirect('adminHome')
              
            else:
                messages.error(request,'username or password not correct')
                return redirect('admin/login/')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'admin_temp/adminLogin.html', {'form': form}) 

def studentregister(request):
    if request.method == 'POST':
        form = registerStudent(request.POST)
        profile_form =profileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # user = Student.objects.create_user(email = email , password = password)
            # user.save()
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            if user is None:
                 messages.error(request,'username or password not correct')
                 return redirect('studentregister')
            elif  user is not None:
                return redirect('adminStudent')
            else:
                messages.error(request,'username or password not correct')
            return redirect('studentregister')
        else:
           messages.error(request,'Error Validating form')
    else:
        form = registerStudent()
        profile_form =profileForm()

    return render(request,'admin_temp/studentregister.html', {'form': form,'profile_form': profile_form})