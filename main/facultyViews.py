import email
from email.message import EmailMessage
from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.urls import is_valid_path
from main.models import UserAccount
from admin_app.models import *
import email
from email.message import EmailMessage
from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from main.admision_models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from itertools import chain
from main.forms import *
import random




def is_faculty(user):
    try:
        return user.is_authenticated and user.is_faculty
    except Faculty.DoesNotExist :
        return False

@user_passes_test(is_faculty,login_url='/general login')
def facultyPage(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    return render(request,'faculty_temp/facultyPage.html',{'profile':profile})

@user_passes_test(is_faculty,login_url='/general login')
def dept_head_page(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    return render(request,'faculty_temp/dept_head_page.html',{'profile':profile})
    
@user_passes_test(is_faculty,login_url='/general login')
def changePasswordFaculty(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    user=Faculty.objects.get(id=request.user.id)
    form = changePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if  new_password != new_password_again and  user.check_password(old_password):  
                messages.error(request,'Two passwords do not match')
                return redirect('changePasswordFaculty')
            elif  new_password == new_password_again and not user.check_password(old_password):
                messages.error(request,'Old password wrong')
                return redirect('changePasswordFaculty')
            elif  new_password == old_password:
                messages.error(request,'Old password and new password same')
                return redirect('changePasswordFaculty')
            elif   new_password == new_password_again and  user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                UserAccount = auth.authenticate(email=user.email, password= new_password)
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('facultyPage')    
            else:
                messages.error(request,'password not correct')
                return redirect('changePasswordFaculty')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'faculty_temp/changePasswordFaculty.html', {'form': form,'profile':profile})