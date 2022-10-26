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
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
import random




def staffMedPage(request):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    return render(request,'staff_med_temp/staffMedPage.html',{'profile':profile})

def changePasswordStaff_med(request):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    user=StaffMed.objects.get(id=request.user.id)
    form = changePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if  new_password != new_password_again and  user.check_password(old_password):  
                messages.error(request,'Two passwords do not match')
                return redirect('changePasswordStaff_med')
            elif  new_password == new_password_again and not user.check_password(old_password):
                messages.error(request,'Old password wrong')
                return redirect('changePasswordStaff_med')
            elif  new_password == old_password:
                messages.error(request,'Old password and new password same')
                return redirect('changePasswordStaff_med')
            elif   new_password == new_password_again and  user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                UserAccount = auth.authenticate(email=user.email, password= new_password)
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffMedPage')    
            else:
                messages.error(request,'password not correct')
                return redirect('changePasswordStaff_med')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'staff_med_temp/changePasswordStaff_med.html', {'form': form,'profile':profile})