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
import random
def is_student(user):
    try:
        return user.is_authenticated and user.is_student 
    except Student.DoesNotExist :
        return False
@user_passes_test(is_student,login_url='/general login')
def studentPage(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    return render(request,'student_temp/studentPage.html',{'profile':profile})

@user_passes_test(is_student,login_url='/general login')
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

@user_passes_test(is_student,login_url='/general login')
def studentCR_notice(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=CRNoticeFilter(request.GET,queryset=student_notice.objects.filter(student_id=profile.email_id).order_by('-date','-time'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/studentCR_notice.html',context=context )

@user_passes_test(is_student,login_url='/general login')
def studentCR_notice_add(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    if request.method == 'POST':
        form = CRNoticeForm(request.POST,request.FILES)
        if form.is_valid() :
            user = form.save(commit=False)
            user.time=datetime.datetime.now().strftime('%H:%M:%S')  
            user.student=profile
            user.section=profile.section
            user.semester=profile.semester
            user.department=profile.department
            user.date=datetime.datetime.now().strftime('%Y-%m-%d')  
            user.save()
            if user is None:
                 messages.error(request,'notice not added')
                 return redirect('studentCR_notice_add')
            elif  user is not None:
                return redirect('studentCR_notice')
            else:
                messages.error(request,'Info not correct')
            return redirect('studentCR_notice_add')
        else:
           messages.error(request,'Error validating registration please try again with correct value')
    else:
        form =CRNoticeForm()

    context['profile']=profile
    context['form']=form
    return render(request,'student_temp/studentCR_notice_add.html', context=context)


@user_passes_test(is_student,login_url='/general login')
def studentCR_notice_delete(request,id):
  object=student_notice.objects.get(id=id)
  object.delete()
  return redirect('studentCR_notice')


@user_passes_test(is_student,login_url='/general login')
def studentCR_notice_update(request,id):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    notice_=student_notice.objects.get(id=id)
    if request.method == 'POST':
        form = CRNoticeForm(request.POST,instance=notice_)

        if form.is_valid():
            content = form.cleaned_data.get('content')
            object=student_notice.objects.get(id=id)
            object.content=content
            object.update=True
            object.update_time=datetime.datetime.now().strftime('%H:%M:%S')  
            object.update_date=datetime.datetime.now().strftime('%Y-%m-%d')  
            object.save()
            if  object is not None:
                return redirect('studentCR_notice')
            else:
                messages.error(request,'enter valid information')
            return redirect('studentCR_notice_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = CRNoticeForm(instance=notice_)

        context['profile']=profile
        context['form']=form
    return render(request,'student_temp/studentCR_notice_update.html', context=context)


@user_passes_test(is_student,login_url='/general login')
def academic_notice(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=CRNoticeFilter(request.GET,queryset=student_notice.objects.filter(department_id=profile.department_id,section=profile.section,semester=profile.semester).order_by('-date','-time'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/academic_notice.html',context=context )

@user_passes_test(is_student,login_url='/general login')
def official_notice(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    std_courses=Enrollment.objects.filter(students_id=profile.email_id)
    course_list=[]
    for i in std_courses:
        course_list.append(i.courses.name)
    final_notice_query=notice.objects.filter(course__name__in=course_list).order_by('-date','-time')
    context={}
    profiles=NoticeFilter(request.GET,queryset=final_notice_query)
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/official_notice.html',context=context )


@user_passes_test(is_student,login_url='/general login')
def medical_logs(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=MedLog.objects.filter(student__email_id=profile.email_id).order_by('-date')
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/medical_logs.html',context=context )

@user_passes_test(is_student,login_url='/general login')
def library_book_status(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=Books.objects.filter(student__email_id=profile.email_id).order_by('-due_date')
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/library_book_status.html',context=context )


@user_passes_test(is_student,login_url='/general login')
def teacher_info(request):
    profile=StudentProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=FacultyProfile.objects.filter(department_id=profile.department_id).order_by('designation_hier','date_of_birth')
    print(profiles)
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)
    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'student_temp/teacher_info.html',context=context )