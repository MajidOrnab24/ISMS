from audioop import add
import email
from email.message import EmailMessage
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
import random

# Admin views here.
def adminHome(request):
    return render(request,'admin_temp/adminHome.html')
    
def adminStudent(request):
    student_profiles=StudentProfile.objects.all()
    query = request.GET.get('q')
    if query:
        student_profiles = StudentProfile.objects.filter(Q(name__icontains=query)
        | Q(department__dept_name__icontains=query)).distinct()
    paginator = Paginator(student_profiles, 1)
    page = request.GET.get('page', 1)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
       profiles = paginator.page(paginator.num_pages)
    context = {
        'profiles': profiles
    }
    return render(request,'admin_temp/adminStudent.html',context )
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
        profile_form =profileForm(request.POST, request.FILES)
        if form.is_valid() and  profile_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name=profile_form.cleaned_data.get('name')
            student_ID=profile_form.cleaned_data.get('student_ID')
            address=profile_form.cleaned_data.get('address')
            father_name=profile_form.cleaned_data.get('father_name')
            mother_name=profile_form.cleaned_data.get('mother_name')
            phone=profile_form.cleaned_data.get('phone')
            semester=profile_form.cleaned_data.get('semester')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            department=profile_form.cleaned_data.get('department')
            session=profile_form.cleaned_data.get('session')
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()
            profile=StudentProfile.objects.get(email=user.id)
            profile.name=name
            profile.father_name=father_name
            profile.student_ID=student_ID
            profile.address=address
            profile.mother_name=mother_name
            profile.phone=phone
            profile.semester=semester
            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.department=department
            profile.session=session
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
