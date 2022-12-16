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
from django.contrib.auth.decorators import login_required,user_passes_test
from itertools import chain
from main.forms import *
from admin_app.forms import *
import random
from admin_app.filters import *
from django.conf import settings
from django.core.mail import send_mail

def is_admin(user):
    try:
        return user.is_authenticated and user.is_superuser 
    except Faculty.DoesNotExist :
        return False
# Admin views here.

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


@user_passes_test(is_admin,login_url='/general login')
def adminHome(request):
    return render(request,'admin_temp/adminHome.html')
@user_passes_test(is_admin,login_url='/general login')   
def changePasswordAdmin(request):
    user= Faculty.objects.get(id=request.user.id)
    form = changePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if new_password != new_password_again and  user.check_password(old_password):  
                messages.error(request,'Two password do not match')
                return redirect('changePasswordAdmin')
            elif new_password == new_password_again and not user.check_password(old_password):
                messages.error(request,'Old password wrong')
                return redirect('changePasswordAdmin')
            elif new_password == old_password:
                messages.error(request,'Old password and new password same')
                return redirect('changePasswordAdmin')
            elif  new_password == new_password_again and  user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                UserAccount = auth.authenticate(email=user.email, password=new_password)
                login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('adminHome')    
            else:
                messages.error(request,'password not correct')
                return redirect('changePasswordAdmin')
        else:
            messages.error(request,'Error Validating form')
    return render(request, 'admin_temp/changePasswordAdmin.html', {'form': form})


# Admin Students views
@user_passes_test(is_admin,login_url='/general login')
def adminStudent(request):
    context={}
    profiles=StudentFilter(request.GET,queryset=StudentProfile.objects.all().order_by('email_id'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminStudent.html',context=context )

@user_passes_test(is_admin,login_url='/general login')
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
            section=profile_form.cleaned_data.get('section')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            cr=profile_form.cleaned_data.get('CR')
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
            profile.section=section
            profile.CR=cr
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
                subject = 'Welcome to IUT '
                message = f'Hi {profile.name}, You are now registered in ISMS as a student of {profile.department}. The student portal of IUT. Your password is {password}. Please change it immediately'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                courses=Courses.objects.filter(semester=profile.semester,department_id=profile.department_id)
                if courses is not None:
                  for course in courses:
                    membership = Enrollment(courses=course,students=profile,date_joined=datetime.datetime.now())
                    membership.save()
                return redirect('adminStudent')
            else:
                messages.error(request,'username or password not correct')
            return redirect('studentregister')
        else:
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = registerStudent()
        profile_form =profileForm()

    return render(request,'admin_temp/studentregister.html', {'form': form,'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def studentChangePass(request,id):
    user=Student.objects.get(id=id)
    form = changePassByadmin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if new_password !=  new_password_again:  
                messages.error(request,'Password1 and Password 2 doesnt match')
                return redirect('studentChangePass')
            elif  new_password ==  new_password_again:
                user.set_password(new_password)
                user.save()
                return redirect('adminStudent')    
            else:
                return redirect('studentChangePass')
        else:
            messages.error(request,'error changing password please provide instructed credentials')

    return render(request, 'admin_temp/studentChangePass.html', {'form': form})
 
@user_passes_test(is_admin,login_url='/general login')
def studentUpdate(request,id):
    student_profile=StudentProfile.objects.get(email_id=id)
    if request.method == 'POST':
        profile_form = profileForm(request.POST, request.FILES,instance=student_profile)
        if  profile_form.is_valid():
            name=profile_form.cleaned_data.get('name')
            student_ID=profile_form.cleaned_data.get('student_ID')
            address=profile_form.cleaned_data.get('address')
            father_name=profile_form.cleaned_data.get('father_name')
            mother_name=profile_form.cleaned_data.get('mother_name')
            phone=profile_form.cleaned_data.get('phone')
            semester=profile_form.cleaned_data.get('semester')
            section=profile_form.cleaned_data.get('section')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            department=profile_form.cleaned_data.get('department')
            cr=profile_form.cleaned_data.get('CR')
            session=profile_form.cleaned_data.get('session')
            profile=StudentProfile.objects.get(email_id=id)
            profile.name=name
            profile.father_name=father_name
            profile.student_ID=student_ID
            profile.address=address
            profile.mother_name=mother_name
            profile.phone=phone
            profile.CR=cr
            profile.section=section
            profile.semester=semester
            
            if(profile.image!=image):
                profile.image.delete()

            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.department=department
            profile.session=session
            profile.save()

            if  profile is not None:
                return redirect('adminStudent')
            else:
                messages.error(request,'enter valid information')
            return redirect('studentUpdate')
        else:
           messages.error(request,'Error validating update form')
    else:
        profile_form =profileForm(instance=student_profile)

    return render(request,'admin_temp/studentUpdate.html', {'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def deleteStudent(request, id):
  student_profile=StudentProfile.objects.get(email_id=id)
  if  student_profile.image:
         student_profile.image.delete()
  student_profile.delete()
  student=Student.objects.get(id=id)
  student.delete()
  return redirect('adminStudent')


# Admin Faculty views
@user_passes_test(is_admin,login_url='/general login')
def adminFaculty(request):
    context={}
    profiles=FacultyFilter(request.GET,queryset=FacultyProfile.objects.all().order_by('email_id'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminFaculty.html',context=context )

@user_passes_test(is_admin,login_url='/general login')
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
            designation=profile_form.cleaned_data.get('designation')
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
            profile.designation=designation
            if designation=='Professor':
                profile.designation_hier=1
            elif designation=='Associate Professor':
                profile.designation_hier=2
            elif designation=='Assistant Professor':
                profile.designation_hier=3
            elif designation=='Lecturer':
                profile.designation_hier=4
            profile.room=room
            profile.education=education
            profile.save()
            if user is None:
                 messages.error(request,'username or password not correct')
                 return redirect('facultyregister')
            elif  user is not None:
                subject = 'Welcome to IUT '
                message = f'Hi {profile.name}, You are now registered in ISMS as a faculty of {profile.department}. The student portal of IUT. Your password is {password}. Please change it immediately after receiving'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                return redirect('adminFaculty')
            else:
                messages.error(request,'username or password not correct')
            return redirect('facultyregister')
        else:
            messages.error(request,'Error validating registrartion please try again with correct value')

    else:
        form = registerFaculty()
        profile_form =facultyprofileform()
    return render(request,'admin_temp/facultyregister.html', {'form': form,'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def facultyUpdate(request,id):
    faculty_profile=FacultyProfile.objects.get(email_id=id)
    if request.method == 'POST':
        profile_form = facultyprofileform(request.POST, request.FILES,instance=faculty_profile)
        if  profile_form.is_valid():
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            designation=profile_form.cleaned_data.get('designation')
            
            department=profile_form.cleaned_data.get('department')
            room =profile_form.cleaned_data.get('room')
            education=profile_form.cleaned_data.get('education')
            profile=FacultyProfile.objects.get(email=id)
            profile.name=name
            profile.address=address
            profile.phone=phone

            if(profile.image!=image):
                profile.image.delete()

            profile.image=image

            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.department=department
            profile.designation=designation
            if designation=='Professor':
                profile.designation_hier=1
            elif designation=='Associate Professor':
                profile.designation_hier=2
            elif designation=='Assistant Professor':
                profile.designation_hier=3
            elif designation=='Lecturer':
                profile.designation_hier=4
            profile.room=room
            profile.education=education
            profile.save()

            if  profile is not None:
                return redirect('adminFaculty')
            else:
                messages.error(request,'enter valid information')
            return redirect('facultyUpdate')
        else:
           messages.error(request,'Error validating update form')
    else:
        profile_form =facultyprofileform(instance=faculty_profile)

    return render(request,'admin_temp/facultyUpdate.html', {'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def deleteFaculty(request, id):
  faculty_profile=FacultyProfile.objects.get(email_id=id)
  if  faculty_profile.image:
         faculty_profile.image.delete()
  faculty_profile.delete()
  faculty=Faculty.objects.get(id=id)
  faculty.delete()
  return redirect('adminFaculty')
@user_passes_test(is_admin,login_url='/general login')
def facultyChangePass(request,id):
    user=Faculty.objects.get(id=id)
    form = changePassByadmin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if new_password !=  new_password_again:  
                messages.error(request,'Password1 and Password 2 doesnt match')
                return redirect('facultyChangePass')
            elif  new_password ==  new_password_again:
                user.set_password(new_password)
                user.save()
                return redirect('adminFaculty')    
            else:
                return redirect('facultyChangePass')
        else:
            messages.error(request,'error changing password please provide instructed credentials')
    return render(request, 'admin_temp/facultyChangePass.html', {'form': form})



# Admin Medical Staff views
@user_passes_test(is_admin,login_url='/general login') 
def adminStaff_med(request):
    context={}
    profiles=StaffMedFilter(request.GET,queryset=StaffMedProfile.objects.all().order_by('email_id'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminStaff_med.html',context=context )

@user_passes_test(is_admin,login_url='/general login')
def staff_med_register(request):
    if request.method == 'POST':
        form = registerStaffMed(request.POST)
        profile_form =staff_med_profileform(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            designation=profile_form.cleaned_data.get('designation')
            duty =profile_form.cleaned_data.get('duty')
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()
            profile=StaffMedProfile.objects.get(email=user.id)
            profile.name=name
            profile.address=address
            profile.phone=phone
            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.designation= designation
            profile.duty=duty
            profile.save()
            if user is None:
                 messages.error(request,'username or password not correct')
                 return redirect('staff_med_register')
            elif  user is not None:
                subject = 'Welcome to IUT '
                message = f'Hi {profile.name}, You are now registered in ISMS as a staff of medical centre in ISMS. The student portal of IUT. Your password is {password}. Please change it immediately after receiving'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                return redirect('adminStaff_med')
            else:
                messages.error(request,'username or password not correct')
            return redirect('staff_med_register')
        else:
            messages.error(request,'Error validating registrartion please try again with correct value')

    else:
        form = registerStaffMed()
        profile_form =staff_med_profileform()
    return render(request,'admin_temp/staff_med_register.html', {'form': form,'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def staff_medChangePass(request,id):
    user=StaffMed.objects.get(id=id)
    form = changePassByadmin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if new_password !=  new_password_again:  
                messages.error(request,'Password1 and Password 2 doesnt match')
                return redirect('staff_medChangePass')
            elif  new_password ==  new_password_again:
                user.set_password(new_password)
                user.save()
                return redirect('adminStaff_med')    
            else:
                return redirect('staff_medChangePass')
        else:
            messages.error(request,'error changing password please provide instructed credentials')
    return render(request, 'admin_temp/staff_medChangePass.html', {'form': form})

@user_passes_test(is_admin,login_url='/general login')
def staff_medUpdate(request,id):
    staff_med_profile=StaffMedProfile.objects.get(email_id=id)
    if request.method == 'POST':
        profile_form = staff_med_profileform(request.POST, request.FILES,instance=staff_med_profile)
        if  profile_form.is_valid():
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            designation=profile_form.cleaned_data.get('designation')
            duty =profile_form.cleaned_data.get('duty')

            profile=StaffMedProfile.objects.get(email=id)
            profile.name=name
            profile.address=address
            profile.phone=phone

            if(profile.image!=image):
                profile.image.delete()

            profile.image=image

            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.designation= designation
            profile.duty=duty

            profile.save()

            if  profile is not None:
                return redirect('adminStaff_med')
            else:
                messages.error(request,'enter valid information')
            return redirect('staff_medUpdate')
        else:
           messages.error(request,'Error validating update form')
    else:
        profile_form = staff_med_profileform(instance=staff_med_profile)

    return render(request,'admin_temp/staff_medUpdate.html', {'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def deleteStaffMed(request, id):
  staff_med_profile=StaffMedProfile.objects.get(email_id=id)
  if  staff_med_profile.image:
         staff_med_profile.image.delete()
  staff_med_profile.delete()
  staff_med=StaffMed.objects.get(id=id)
  staff_med.delete()
  return redirect('adminStaff_med')




# Admin Library Staff views

@user_passes_test(is_admin,login_url='/general login') 
def adminStaff_lib(request):
    context={}
    profiles=StaffLibFilter(request.GET,queryset=StaffLibProfile.objects.all().order_by('email_id'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admin_temp/adminStaff_lib.html',context=context )

@user_passes_test(is_admin,login_url='/general login')
def staff_lib_register(request):
    if request.method == 'POST':
        form = registerStaffLib(request.POST)
        profile_form =staff_lib_profileform(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            designation=profile_form.cleaned_data.get('designation')
            duty =profile_form.cleaned_data.get('duty')
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()
            profile=StaffLibProfile.objects.get(email=user.id)
            profile.name=name
            profile.address=address
            profile.phone=phone
            profile.image=image
            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.designation= designation
            profile.duty=duty
            profile.save()
            if user is None:
                 messages.error(request,'username or password not correct')
                 return redirect('staff_lib_register')
            elif  user is not None:
                subject = 'Welcome to IUT '
                message = f'Hi {profile.name}, You are now registered in ISMS as a staff of IUT Central Library in ISMS. The student portal of IUT. Your password is {password}. Please change it immediately after receiving'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                return redirect('adminStaff_lib')
            else:
                messages.error(request,'username or password not correct')
            return redirect('staff_lib_register')
        else:
            messages.error(request,'Error validating registrartion please try again with correct value')

    else:
        form = registerStaffLib()
        profile_form =staff_lib_profileform()
    return render(request,'admin_temp/staff_lib_register.html', {'form': form,'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def staff_libUpdate(request,id):
    staff_med_profile=StaffLibProfile.objects.get(email_id=id)
    if request.method == 'POST':
        profile_form = staff_lib_profileform(request.POST, request.FILES,instance=staff_med_profile)
        if  profile_form.is_valid():
            name=profile_form.cleaned_data.get('name')
            address=profile_form.cleaned_data.get('address')
            phone=profile_form.cleaned_data.get('phone')
            image=profile_form.cleaned_data.get('image')
            gender=profile_form.cleaned_data.get('gender')
            date_of_birth=profile_form.cleaned_data.get('date_of_birth')
            designation=profile_form.cleaned_data.get('designation')
            duty =profile_form.cleaned_data.get('duty')

            profile=StaffLibProfile.objects.get(email=id)
            profile.name=name
            profile.address=address
            profile.phone=phone

            if(profile.image!=image):
                profile.image.delete()

            profile.image=image

            profile.gender=gender
            profile.date_of_birth=date_of_birth
            profile.designation= designation
            profile.duty=duty

            profile.save()

            if  profile is not None:
                return redirect('adminStaff_lib')
            else:
                messages.error(request,'enter valid information')
            return redirect('staff_libUpdate')
        else:
           messages.error(request,'Error validating update form')
    else:
        profile_form = staff_med_profileform(instance=staff_med_profile)

    return render(request,'admin_temp/staff_libUpdate.html', {'profile_form': profile_form})

@user_passes_test(is_admin,login_url='/general login')
def deleteStaffLib(request, id):
  staff_lib_profile=StaffLibProfile.objects.get(email_id=id)
  if  staff_lib_profile.image:
         staff_lib_profile.image.delete()
  staff_lib_profile.delete()
  staff_lib=StaffLib.objects.get(id=id)
  staff_lib.delete()
  return redirect('adminStaff_lib')

@user_passes_test(is_admin,login_url='/general login')
def staff_libChangePass(request,id):
    user=StaffLib.objects.get(id=id)
    form = changePassByadmin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            new_password_again = form.cleaned_data.get('new_password_again')
            if new_password !=  new_password_again:  
                messages.error(request,'Password1 and Password 2 doesnt match')
                return redirect('staff_medChangePass')
            elif  new_password ==  new_password_again:
                user.set_password(new_password)
                user.save()
                return redirect('adminStaff_lib')    
            else:
                return redirect('staff_libChangePass')
        else:
            messages.error(request,'error changing password please provide instructed credentials')
    return render(request, 'admin_temp/staff_libChangePass.html', {'form': form})

# Admission info edit views

@user_passes_test(is_admin,login_url='/general login')
def admin_roadmap(request):
    context={}
    profiles=RoadmapFilter(request.GET,queryset=RoadMap.objects.all().order_by('date'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admission_temp/admin_roadmap.html',context=context )

@user_passes_test(is_admin,login_url='/general login')
def roadmap_add(request):
    if request.method == 'POST':
        form = roadMapForm(request.POST)
        if form.is_valid() :
            event = form.cleaned_data.get('event')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            user = form.save(commit=False)
            user.save()
            if user is None:
                 messages.error(request,'roadmap not added')
                 return redirect('roadmap_add')
            elif  user is not None:
                return redirect('admin_roadmap')
            else:
                messages.error(request,'Info not correct')
            return redirect('roadmap_add')
        else:
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = roadMapForm()

    return render(request,'admission_temp/roadmap_add.html', {'form': form}) 

@user_passes_test(is_admin,login_url='/general login')
def delete_roadmap(request, id):
  roadmap=RoadMap.objects.get(id=id)
  roadmap.delete()
  return redirect('admin_roadmap')
@user_passes_test(is_admin,login_url='/general login')
def update_roadmap(request, id):
    roadmap=RoadMap.objects.get(id=id)
    if request.method == 'POST':
        form = roadMapForm(request.POST,instance=roadmap)
        if form.is_valid():
            event = form.cleaned_data.get('event')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            object=RoadMap.objects.get(id=id)
            object.event=event
            object.date=date
            object.time=time
            object.save()
            if  object is not None:
                return redirect('admin_roadmap')
            else:
                messages.error(request,'enter valid information')
            return redirect('update_roadmap')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = roadMapForm(instance=roadmap)

    return render(request,'admission_temp/update_roadmap.html', {'form': form})

@user_passes_test(is_admin,login_url='/general login')
def admin_faq(request):
    context={}
    profiles=FaqFilter(request.GET,queryset=Faq.objects.all().order_by('id'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    return render(request,'admission_temp/admin_faq.html',context=context )
@user_passes_test(is_admin,login_url='/general login')
def delete_faq(request, id):
  faq=Faq.objects.get(id=id)
  faq.delete()
  return redirect('admin_faq')

@user_passes_test(is_admin,login_url='/general login')
def faq_add(request):
    if request.method == 'POST':
        form = faqForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.save()
            if user is None:
                 messages.error(request,'faq not added')
                 return redirect('faq_add')
            elif  user is not None:
                return redirect('admin_faq')
            else:
                messages.error(request,'Info not correct')
            return redirect('faq_add')
        else:
           messages.error(request,'Error validating registrartion please try again with correct value')
    else:
        form = faqForm()

    return render(request,'admission_temp/faq_add.html', {'form': form}) 

@user_passes_test(is_admin,login_url='/general login')
def update_faq(request, id):
    faq=Faq.objects.get(id=id)
    if request.method == 'POST':
        form = faqForm(request.POST,instance=faq)
        if form.is_valid():
            question = form.cleaned_data.get('question')
            answer = form.cleaned_data.get('answer')
            object=Faq.objects.get(id=id)
            object.question=question
            object.answer=answer
            object.save()
            if  object is not None:
                return redirect('admin_faq')
            else:
                messages.error(request,'enter valid information')
            return redirect('update_faq')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = faqForm(instance=faq)

    return render(request,'admission_temp/update_faq.html', {'form': form})