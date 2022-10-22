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
import random
from admin_app.filters import *


# Admin views here.


@login_required
def adminHome(request):
    return render(request,'admin_temp/adminHome.html')
@login_required
def deleteStudent(request, id):
  student_profile=StudentProfile.objects.get(email_id=id)
  if  student_profile.image:
         student_profile.image.delete()
  student_profile.delete()
  student=Student.objects.get(id=id)
  student.delete()
  return redirect('adminStudent')
@login_required
def deleteFaculty(request, id):
  faculty_profile=FacultyProfile.objects.get(email_id=id)
  if  faculty_profile.image:
         faculty_profile.image.delete()
  faculty_profile.delete()
  faculty=Faculty.objects.get(id=id)
  faculty.delete()
  return redirect('adminFaculty')
@login_required  
def adminStudent(request):
    context={}
    profiles=StudentFilter(request.GET,queryset=StudentProfile.objects.all())
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminStudent.html',context=context )
@login_required
def adminFaculty(request):
    context={}
    profiles=FacultyFilter(request.GET,queryset=FacultyProfile.objects.all())
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminFaculty.html',context=context )
    
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

            if UserAccount is not None and not UserAccount.is_admin:
                if UserAccount.is_admin:
                   types='Admin'
                else:
                   types=UserAccount.type
                messages.error(request,'Wrong user type, Admin only. '+types.title()+' type not accepted')
                return redirect('admin/login/')

            elif UserAccount is not None and  UserAccount.is_admin:
                  login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                  return redirect('adminHome')
              
            else:
                messages.error(request,'username or password not correct')
                return redirect('admin/login/')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'admin_temp/adminLogin.html', {'form': form}) 
@login_required
def studentUpdate(request,id):
    student_profile=StudentProfile.objects.get(email_id=id)
    student=Student.objects.get(id=id)
    if request.method == 'POST':
        form = updateStudentForm(request.POST,instance=student)
        profile_form = profileForm(request.POST, request.FILES,instance=student_profile)
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
            profile=StudentProfile.objects.get(email_id=user.id)
            profile.name=name
            profile.father_name=father_name
            profile.student_ID=student_ID
            profile.address=address
            profile.mother_name=mother_name
            profile.phone=phone
            profile.semester=semester
            
            if(profile.image!=image):
                profile.image.delete()

            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.department=department
            profile.session=session
            profile.save()
            if  student is None:
                 messages.error(request,'username or password not correct')
                 return redirect('studentUpdate')
            elif  student is not None:
                return redirect('adminStudent')
            else:
                messages.error(request,'username or password not correct')
            return redirect('studentUpdate')
        else:
           user.delete()
           messages.error(request,'Error Validating form')
    else:
        form = updateStudentForm(instance=student)
        profile_form =profileForm(instance=student_profile)

    return render(request,'admin_temp/studentUpdate.html', {'form': form,'profile_form': profile_form})

@login_required
def facultyregister(request):
    if request.method == 'POST':
        form = registerFaculty(request.POST)
        profile_form =facultyprofileform(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            department=profile_form.cleaned_data.get('department')
            room =profile_form.cleaned_data.get('room')
            education=profile_form.cleaned_data.get('education')
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()
            profile=FacultyProfile.objects.get(email=user.id)
            profile.name=name
            profile.address=address
            profile.phone=phone
            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.department=department
            profile.room=room
            profile.education=education
            profile.save()
            if user is None:
                 messages.error(request,'username or password not correct')
                 return redirect('facultyregister')
            elif  user is not None:
                return redirect('adminFaculty')
            else:
                messages.error(request,'username or password not correct')
            return redirect('facultyregister')
        else:
            user.delete()
            messages.error(request,'Error validating registrartion please try again with correct value')

    else:
        form = registerFaculty()
        profile_form =facultyprofileform()
    return render(request,'admin_temp/facultyregister.html', {'form': form,'profile_form': profile_form})




@login_required
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
           user.delete()
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = registerStudent()
        profile_form =profileForm()

    return render(request,'admin_temp/studentregister.html', {'form': form,'profile_form': profile_form})


