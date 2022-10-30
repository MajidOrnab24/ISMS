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
def studentCR_page(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    return render(request,'student_temp/studentCR_page.html',{'profile':profile})
def changePasswordStudent(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    user=Student.objects.get(id=request.user.id)
    form = changePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if  new_password != new_password_again and  user.check_password(old_password):  
                messages.error(request,'Two passwords do not match')
                return redirect('changePasswordStudent')
            elif  new_password == new_password_again and not user.check_password(old_password):
                messages.error(request,'Old password wrong')
                return redirect('changePasswordStudent')
            elif  new_password == old_password:
                messages.error(request,'Old password and new password same')
                return redirect('changePasswordStudent')
            elif   new_password == new_password_again and  user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                UserAccount = auth.authenticate(email=user.email, password= new_password)
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('studentPage')    
            else:
                messages.error(request,'password not correct')
                return redirect('changePasswordStudent')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'student_temp/changePasswordStudent.html', {'form': form,'profile':profile})