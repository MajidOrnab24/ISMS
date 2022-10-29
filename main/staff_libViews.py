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
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
from admin_app.forms import *
from main.admission_forms import *
import random
from admin_app.filters import *
from django.conf import settings
from django.core.mail import send_mail



@login_required
def staffLibPage(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    return render(request,'staff_lib_temp/staffLibPage.html',{'profile':profile})
@login_required
def changePasswordStaff_lib(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    user=StaffLib.objects.get(id=request.user.id)
    form = changePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if  new_password != new_password_again and  user.check_password(old_password):  
                messages.error(request,'Two passwords do not match')
                return redirect('changePasswordStaff_lib')
            elif  new_password == new_password_again and not user.check_password(old_password):
                messages.error(request,'Old password wrong')
                return redirect('changePasswordStaff_lib')
            elif  new_password == old_password:
                messages.error(request,'Old password and new password same')
                return redirect('changePasswordStaff_lib')
            elif   new_password == new_password_again and  user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                UserAccount = auth.authenticate(email=user.email, password= new_password)
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('staffLibPage')    
            else:
                messages.error(request,'password not correct')
                return redirect('changePasswordStaff_lib')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'staff_lib_temp/changePasswordStaff_lib.html', {'form': form,'profile':profile})

@login_required
def admissionQuestion(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=AdmissionQuestionFilter(request.GET,queryset=QuestionBank.objects.all())
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/admissionQuestion.html',context=context )

@login_required
def admissionQuestion_add(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    if request.method == 'POST':
        form = questionBankForm(request.POST,request.FILES)
        if form.is_valid() :
            user = form.save(commit=False)
            user.save()
            if user is None:
                 messages.error(request,'question not added')
                 return redirect('admissionQuestion_add')
            elif  user is not None:
                return redirect('admissionQuestion')
            else:
                messages.error(request,'Info not correct')
            return redirect('admissionQuestion_add')
        else:
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = questionBankForm()

    return render(request,'staff_lib_temp/admissionQuestion_add.html', {'form': form,'profile':profile}) 

@login_required
def admissionQuestion_update(request, id):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    question=QuestionBank.objects.get(id=id)
    if request.method == 'POST':
        form = questionBankForm(request.POST,request.FILES,instance=question)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            file = form.cleaned_data.get('file')
            object=QuestionBank.objects.get(id=id)
            object.year=year
            if(object.file!=file):
                object.file.delete()
            object.file=file
            object.save()
            if  object is not None:
                return redirect('admissionQuestion')
            else:
                messages.error(request,'enter valid information')
            return redirect('admissionQuestion_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = questionBankForm(instance=question)

    return render(request,'staff_lib_temp/admissionQuestion_update.html', {'form': form,'profile':profile})

@login_required
def admissionQuestion_delete(request, id):
  question=QuestionBank.objects.get(id=id)
  if  question.file:
          question.file.delete()
  question.delete()
  return redirect('admissionQuestion')

@login_required
def semesterQuestion(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=semesterQuestionFilter(request.GET,queryset=SemesterQuestionBank.objects.all())
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/semesterQuestion.html',context=context )


@login_required
def semesterQuestion_delete(request, id):
  question=SemesterQuestionBank.objects.get(id=id)
  if  question.file:
          question.file.delete()
  question.delete()
  return redirect('semesterQuestion')

@login_required
def semesterQuestion_add(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    if request.method == 'POST':
        form = semesterQuestionBankForm(request.POST,request.FILES)
        if form.is_valid() :
            user = form.save(commit=False)
            user.save()
            if user is None:
                 messages.error(request,'question not added')
                 return redirect('semesterQuestion_add')
            elif  user is not None:
                return redirect('semesterQuestion')
            else:
                messages.error(request,'Info not correct')
            return redirect('semesterQuestion_add')
        else:
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = semesterQuestionBankForm()

    return render(request,'staff_lib_temp/semesterQuestion_add.html', {'form': form,'profile':profile}) 

@login_required
def semesterQuestion_update(request, id):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    question=SemesterQuestionBank.objects.get(id=id)
    if request.method == 'POST':
        form = semesterQuestionBankForm(request.POST,request.FILES,instance=question)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            department=form.cleaned_data.get('department')
            semester=form.cleaned_data.get('semester')
            file = form.cleaned_data.get('file')
            object=SemesterQuestionBank.objects.get(id=id)
            object.year=year
            if(object.file!=file):
                object.file.delete()
            object.file=file
            object.department=department
            object.semester=semester
            object.save()
            if  object is not None:
                return redirect('semesterQuestion')
            else:
                messages.error(request,'enter valid information')
            return redirect('semesterQuestion_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = semesterQuestionBankForm(instance=question)

    return render(request,'staff_lib_temp/semesterQuestion_update.html', {'form': form,'profile':profile})