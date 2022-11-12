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




def is_faculty(user):
    try:
        return user.is_authenticated and user.is_faculty and not user.is_admin
    except Faculty.DoesNotExist :
        return False



@user_passes_test(is_faculty,login_url='/general login')
def facultyPage(request):
    is_head=False
    head=DeptHeadFaculty.objects.get(dept_id= request.user.facultyprofile.department_id)
    if(head.email):
        if(head.email.email.email==request.user.email):
            is_head=True
        else:
            is_head=False
    context={}
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    context['profile']=profile
    context['is_head']=is_head
    return render(request,'faculty_temp/facultyPage.html',context=context)
   
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

@user_passes_test(is_faculty,login_url='/general login')
def courses(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    is_head=False
    head=DeptHeadFaculty.objects.get(dept_id= request.user.facultyprofile.department_id)
    if(head.email):
        if(head.email.email.email==request.user.email):
            is_head=True
        else:
            is_head=False
    context={}
    profiles=CoursesFilter(request.GET,queryset=Courses.objects.filter(created_d_ID=profile.department.dept_id).order_by('semester'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    context['is_head']=is_head
    return render(request,'faculty_temp/courses.html',context=context )

@user_passes_test(is_faculty,login_url='/general login')
def courses_add(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    is_head=False
    head=DeptHeadFaculty.objects.get(dept_id= request.user.facultyprofile.department_id)
    if(head.email):
        if(head.email.email.email==request.user.email):
            is_head=True
        else:
            is_head=False
    context={}
    if request.method == 'POST':
        form = CoursesForm(request.POST,request.FILES)
        form.fields['faculty'].queryset = FacultyProfile.objects.filter(department=request.user.facultyprofile.department_id)
        if form.is_valid() :
            user = form.save(commit=False)
            user.created_d_ID=request.user.facultyprofile.department_id
            user.save()
            if user is None:
                 messages.error(request,'course not added')
                 return redirect('courses_add')
            elif  user is not None:
                return redirect('courses')
            else:
                messages.error(request,'Info not correct')
            return redirect('courses_add')
        else:
           messages.error(request,'Error validating registration please try again with correct value')
    else:
        form =CoursesForm()
        form.fields['faculty'].queryset = FacultyProfile.objects.filter(department=request.user.facultyprofile.department_id)
    context['profile']=profile
    context['is_head']=is_head
    context['form']=form
    return render(request,'faculty_temp/courses_add.html', context=context)

@user_passes_test(is_faculty,login_url='/general login')
def courses_update(request, id):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    is_head=False
    head=DeptHeadFaculty.objects.get(dept_id= request.user.facultyprofile.department_id)
    if(head.email):
        if(head.email.email.email==request.user.email):
            is_head=True
        else:
            is_head=False
    context={}
    course=Courses.objects.get(id=id)
    if request.method == 'POST':
        form = CoursesForm(request.POST,instance=course)
        form.fields['faculty'].queryset = FacultyProfile.objects.filter(department=request.user.facultyprofile.department_id)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            semester=form.cleaned_data.get('semester')
            credit=form.cleaned_data.get('credit')
            faculty = form.cleaned_data.get('faculty')
            department=form.cleaned_data.get('department')
            object=Courses.objects.get(id=id)
            object.name=name
            object.semester=semester
            object.credit=credit
            object.faculty=faculty
            object.department=department
            object.save()
            if  object is not None:
                return redirect('courses')
            else:
                messages.error(request,'enter valid information')
            return redirect('courses_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = CoursesForm(instance=course)
        form.fields['faculty'].queryset = FacultyProfile.objects.filter(department=request.user.facultyprofile.department_id)

        context['profile']=profile
        context['is_head']=is_head
        context['form']=form
    return render(request,'faculty_temp/courses_update.html', context=context)


@user_passes_test(is_faculty,login_url='/general login')
def courses_delete(request, id):
  course=Courses.objects.get(id=id)
  course.delete()
  return redirect('courses')

@user_passes_test(is_faculty,login_url='/general login')
def assigned_courses(request):
    profile=FacultyProfile.objects.get(email_id=request.user.id)
    is_head=False
    head=DeptHeadFaculty.objects.get(dept_id= request.user.facultyprofile.department_id)
    if(head.email):
        if(head.email.email.email==request.user.email):
            is_head=True
        else:
            is_head=False
    context={}
    profiles=CoursesFilter(request.GET,queryset=Courses.objects.filter(faculty=profile).order_by('semester'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    context['is_head']=is_head
    return render(request,'faculty_temp/assigned_courses.html',context=context )
    

