from audioop import add
import email
from email.message import EmailMessage
from multiprocessing import context
from pickle import TRUE
import profile
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from itertools import chain
from main.forms import *
from admin_app.forms import *
from main.admission_forms import *
import random
from admin_app.filters import *
from django.conf import settings
from django.core.mail import send_mail
import string


def is_staffMed(user):
    try:
        return user.is_authenticated and user.is_staff_med 
    except StaffMed.DoesNotExist :
        return False

@user_passes_test(is_staffMed,login_url='/general login')
def staffMedPage(request):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    return render(request,'staff_med_temp/staffMedPage.html',{'profile':profile})

@user_passes_test(is_staffMed,login_url='/general login')
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

@user_passes_test(is_staffMed,login_url='/general login')
def medlogs(request):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=MedLogsFilter(request.GET,queryset=MedLog.objects.all().order_by('date'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_med_temp/medlogs.html',context=context )

@user_passes_test(is_staffMed,login_url='/general login')
def medlogs_add(request):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    if request.method == 'POST':
        form = medlogsForm(request.POST,request.FILES)
        if form.is_valid() :
            id = form.cleaned_data.get('student_id')
            try:
                student=StudentProfile.objects.get(student_ID=id)
            except StudentProfile.DoesNotExist:
                  msg='Student with id '+str(id)+' does not exist'
                  messages.error(request,msg)
                  return redirect('medlogs_add')
            user = form.save(commit=False)
            user.student=student
            user.save()
            if user is None:
                 messages.error(request,'medical info not added')
                 return redirect('medlogs_add')
            elif  user is not None:
                return redirect('medlogs')
            else:
                messages.error(request,'Info not correct')
            return redirect('medlogs_add')
        else:
           messages.error(request,'Error validating registration please try again with correct value')
    else:
        form = medlogsForm()

    return render(request,'staff_med_temp/medlogs_add.html', {'form': form,'profile':profile})

@user_passes_test(is_staffMed,login_url='/general login')
def medlogs_update(request, id):
    profile=StaffMedProfile.objects.get(email_id=request.user.id)
    log=MedLog.objects.get(id=id)
    if request.method == 'POST':
        form = medlogsUpdateForm(request.POST,instance=log)
        if form.is_valid():
            disease = form.cleaned_data.get('disease')
            referred_by=form.cleaned_data.get('referred_by')
            details=form.cleaned_data.get('details')
            remuneration_date = form.cleaned_data.get('remuneration_date')
            remuneration = form.cleaned_data.get('remuneration')
            object=MedLog.objects.get(id=id)
            object.disease=disease
            object.referred_by=referred_by
            object.remuneration_date=remuneration_date
            object.remuneration=remuneration
            object.details=details
            object.save()
            if  object is not None:
                return redirect('medlogs')
            else:
                messages.error(request,'enter valid information')
            return redirect('medlogs_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form =  medlogsUpdateForm(instance=log)

    return render(request,'staff_med_temp/medlogs_update.html', {'form': form,'profile':profile})

@user_passes_test(is_staffMed,login_url='/general login')
def medlogs_delete(request, id):
  log=MedLog.objects.get(id=id)
  log.delete()
  return redirect('medlogs')