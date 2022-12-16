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
def is_staffLib(user):
    try:
        return user.is_authenticated and user.is_staff_lib 
    except StaffLib.DoesNotExist :
        return False


def get_book_code():
    length=8
    letter=string.ascii_lowercase+'unique'
    letters = letter.lower()+ string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@user_passes_test(is_staffLib,login_url='/general login')
def staffLibPage(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    return render(request,'staff_lib_temp/staffLibPage.html',{'profile':profile})
@user_passes_test(is_staffLib,login_url='/general login')
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

@user_passes_test(is_staffLib,login_url='/general login')
def admissionQuestion(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=AdmissionQuestionFilter(request.GET,queryset=QuestionBank.objects.all().order_by('year'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/admissionQuestion.html',context=context )

@user_passes_test(is_staffLib,login_url='/general login')
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

@user_passes_test(is_staffLib,login_url='/general login')
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

@user_passes_test(is_staffLib,login_url='/general login')
def admissionQuestion_delete(request, id):
  question=QuestionBank.objects.get(id=id)
  if  question.file:
          question.file.delete()
  question.delete()
  return redirect('admissionQuestion')

@user_passes_test(is_staffLib,login_url='/general login')
def semesterQuestion(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=semesterQuestionFilter(request.GET,queryset=SemesterQuestionBank.objects.all().order_by('year'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/semesterQuestion.html',context=context )


@user_passes_test(is_staffLib,login_url='/general login')
def semesterQuestion_delete(request, id):
  question=SemesterQuestionBank.objects.get(id=id)
  if  question.file:
          question.file.delete()
  question.delete()
  return redirect('semesterQuestion')

@user_passes_test(is_staffLib,login_url='/general login')
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

@user_passes_test(is_staffLib,login_url='/general login')
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

@user_passes_test(is_staffLib,login_url='/general login')
def lib_books(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=BooksFilter(request.GET,queryset=Books.objects.all().order_by('shelf_no'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/lib_books.html',context=context )

@user_passes_test(is_staffLib,login_url='/general login')
def lib_books_add(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    if request.method == 'POST':
        form = bookForm(request.POST,request.FILES)
        if form.is_valid() :
            book_code=get_book_code()
            user = form.save(commit=False)
            user.book_code=book_code
            user.save()
            if user is None:
                 messages.error(request,'book not added')
                 return redirect('lib_books_add')
            elif  user is not None:
                return redirect('lib_books')
            else:
                messages.error(request,'Info not correct')
            return redirect('lib_books_add')
        else:
           messages.error(request,'Error validating registration please try again with correct value')
    else:
        form = bookForm()

    return render(request,'staff_lib_temp/lib_books_add.html', {'form': form,'profile':profile})

@user_passes_test(is_staffLib,login_url='/general login')
def lib_books_delete(request, id):
  book=Books.objects.get(id=id)
  book.delete()
  return redirect('lib_books')

@user_passes_test(is_staffLib,login_url='/general login')
def lib_books_update(request, id):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    book=Books.objects.get(id=id)
    if request.method == 'POST':
        form = bookForm(request.POST,instance=book)
        if form.is_valid():
            author = form.cleaned_data.get('author')
            title=form.cleaned_data.get('title')
            shelf_no=form.cleaned_data.get('shelf_no')
            category = form.cleaned_data.get('category')
            object=Books.objects.get(id=id)
            object.author=author
            object.category=category
            object.title=title
            object.shelf_no=shelf_no
            object.save()
            if  object is not None:
                return redirect('lib_books')
            else:
                messages.error(request,'enter valid information')
            return redirect('lib_books_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = bookForm(instance=book)

    return render(request,'staff_lib_temp/lib_books_update.html', {'form': form,'profile':profile})


@user_passes_test(is_staffLib,login_url='/general login')
def books_student(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    context={}
    profiles=BooksStudentFilter(request.GET,queryset=Books.objects.exclude(student__isnull=True).order_by('shelf_no'))
    context['profiles']=profiles
    paginated_profiles=Paginator(profiles.qs,3)
    page_number=request.GET.get('page')
    profile_page_obj=paginated_profiles.get_page(page_number)

    context['profile_page_obj']=profile_page_obj
    context['profile']=profile
    return render(request,'staff_lib_temp/books_student.html',context=context )

@user_passes_test(is_staffLib,login_url='/general login')
def books_student_delete(request, id):
  book=Books.objects.get(id=id)
  book.student=None
  book.borrow_date=None
  book.due_date=None
  book.save()
  return redirect('books_student')

@user_passes_test(is_staffLib,login_url='/general login')
def books_student_add(request):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    if request.method == 'POST':
        form = StudentbookForm(request.POST,request.FILES)
        if form.is_valid() :
            student_ID = form.cleaned_data.get('student_ID')
            borrow_date=form.cleaned_data.get('borrow_date')
            due_date=form.cleaned_data.get('due_date')
            book_code=form.cleaned_data.get('book_code')
            exist=Books.objects.filter(book_code=book_code).exists()
            if exist==False:
                 messages.error(request,'book not found')
                 return redirect('books_student_add')
            elif  exist==True:
                std_exist=StudentProfile.objects.filter(student_ID=student_ID).exists()
                book=Books.objects.get(book_code=book_code)
                book_std=book.student
                if std_exist==True and book_std is not None:
                    msg='dsfuikhgudk'
                    msg=book.title+' has already been issued to:'
                    messages.error(request,msg)
                    messages.error(request, f'{"Name: "}{book.student.name}')
                    messages.error(request, f'{"Student ID: "}{book.student.student_ID}')
                    msg='Please come back after '+str(book.due_date.strftime("%d-%B-%Y"))+ ' hopefully'
                    messages.error(request,msg)



                    return redirect('books_student_add')  
                elif std_exist ==True and book_std is None:
                    count = Books.objects.filter(student_id__student_ID=student_ID).count()
                    if count>=5 :
                     messages.error(request,'Student already has five book issued')
                     return redirect('books_student_add')
                    else:
                     object=Books.objects.get(book_code=book_code)
                     student=StudentProfile.objects.get(student_ID=student_ID)
                     object.due_date= due_date
                     object.borrow_date=borrow_date
                     object.student=student
                     object.save()
                    return redirect('books_student')
                else:
                    msg=student_ID+' student does not exist'
                    messages.error(request,msg)
                    return redirect('books_student_add')
               
            else:
                messages.error(request,'Info not correct')
            return redirect('books_student_add_add')
        else:
           messages.error(request,'Error validating registration please try again with correct value')
    else:
        form = StudentbookForm()

    return render(request,'staff_lib_temp/books_student_add.html', {'form': form,'profile':profile})

@user_passes_test(is_staffLib,login_url='/general login')
def books_student_update(request, id):
    profile=StaffLibProfile.objects.get(email_id=request.user.id)
    book=Books.objects.get(id=id)
    if request.method == 'POST':
        form = bookupdateform(request.POST,instance=book)
        if form.is_valid():
            borrow_date = form.cleaned_data.get('borrow_date')
            due_date=form.cleaned_data.get('due_date')
            object=Books.objects.get(id=id)
            object.due_date=due_date
            object.borrow_date=borrow_date
            object.save()
            if  object is not None:
                return redirect('books_student')
            else:
                messages.error(request,'enter valid information')
            return redirect('books_student_update')
        else:
           messages.error(request,'Error validating update form')
    else:
        form = bookupdateform(instance=book)

    return render(request,'staff_lib_temp/books_student_update.html', {'form': form,'profile':profile,'book':book})