from django.contrib import messages, auth
from django.shortcuts import redirect, render
import os

from admin_app.forms import signinformAdmin
from main.admission_forms import *
from main.admision_models import *

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
                    return redirect('viewroadmap')

                elif UserAccount is not None and  UserAccount.is_admin:
                    # print(UserAccount.type)
                      auth.login(request,  UserAccount,backend='django.contrib.auth.backends.ModelBackend')
                      return redirect('viewroadmap')

                else:
                    messages.error(request,'username or password not correct')
                    return redirect('/login/')
            else:
                messages.error(request,'Error Validating form')
    return render(request, 'admin_temp/adminLogin.html')
def adminLogout(request):
    auth.logout(request)
    return redirect("login")
def setroadmap(request):
    if request.method == 'POST':
        info = roadMapForm(request.POST)
        if info.is_valid():
            ev = request.POST['event']
            dt = request.POST['date']
            tm = request.POST['time']
            value = RoadMap(event=ev,date=dt,time=tm)
            value.save()
            messages.success(request,"Data Insert Successfully")
            return redirect('viewroadmap')
        else:
            messages.error(request,"Invalid Input")
            return redirect('setroadmap')
    form = roadMapForm()
    context = {
        'form':form
    }
    return render(request,'admin_temp/setRoadMap.html',context)

def viewroadmap(request):
    info = RoadMap.objects.all()
    context = {
        'query': info
    }
    return render(request, 'admin_temp/viewRoadMap.html', context)
def editroadmap(request,id):
    item = RoadMap.objects.get(id=id)
    if request.method == 'POST':
        item.event = request.POST['event']
        item.date = request.POST['date']
        item.time = request.POST['time']
        item.save()
        messages.success(request,"Data Update Successfully")
        return redirect('viewroadmap')
    forms = roadMapForm(instance=item)
    context = {
        'form':forms,
        'id':id,
    }
    return render(request, 'admin_temp/editRoadMap.html', context)
def deleteroadmap(request,id):
    item = RoadMap.objects.get(id=id)
    item.delete()
    messages.success(request,"Data Delete Succefully")
    return redirect('viewroadmap')

def setfaq(request):
    if request.method == 'POST':
        info = faqForm(request.POST)
        if info.is_valid():
            qs = request.POST['question']
            ans = request.POST['answer']

            value = Faq(question=qs,answer=ans)
            value.save()
            messages.success(request,"Data Insert Successfully")
            return redirect('viewfaq')
        else:
            messages.error(request,"Invalid Input")
            return redirect('setfaq')
    form = faqForm()
    context = {
        'form': form
    }
    return render(request, 'admin_temp/setFaq.html', context)
def viewfaq(request):
    info = Faq.objects.all()
    context = {
        'query': info
    }
    return render(request, 'admin_temp/viewFaq.html', context)
def editfaq(request,id):
    item = Faq.objects.get(id=id)
    if request.method == 'POST':
        item.question = request.POST['question']
        item.answer = request.POST['answer']
        item.save()
        messages.success(request, "Data Update Successfully")
        return redirect('viewfaq')
    forms = faqForm(instance=item)
    context = {
        'form': forms,
        'id': id,
    }
    return render(request, 'admin_temp/editFaq.html', context)
def deletefaq(request,id):
    delItem = Faq.objects.get(id=id)
    delItem.delete()
    messages.success(request,"Data Delete Successfully")
    return redirect('viewfaq')

def setquestionbank(request):
    if request.method == 'POST':
        info = questionBankForm(request.POST,request.FILES)
        if info.is_valid():
            year = request.POST['year']
            file = request.FILES['file']
            value = QuestionBank(year=year,file=file)
            value.save()
            messages.success(request, "Data Insert Successfully")
            return redirect('viewquestionbank')
        else:
            messages.error(request, "Invalid Input")
            return redirect('setquestionbank')
    form = questionBankForm()
    context = {
        'form':form,
    }
    return render(request,'admin_temp/setQuestionBank.html',context)
def editquestionbank(request,id):
    item = QuestionBank.objects.get(id=id)
    if request.method == 'POST':
        item.year = request.POST['year']
        item.save()
        if request.FILES['file']:
            delpath = "static/media/" + str(item.file)
            os.remove(delpath)
            item.file = request.FILES['file']
            item.save()
        else:
            pass
        messages.success(request, "Data Update Successfully")
        return redirect('viewquestionbank')
    forms = questionBankForm(instance=item)
    context = {
        'form': forms,
        'id': id,
        'item':item,
    }
    return render(request,'admin_temp/editQuestionBank.html',context)
def viewquestionbank(request):
    info = QuestionBank.objects.all()
    context = {
        'query': info
    }
    return render(request,'admin_temp/viewQuestionBank.html',context)
def deletequestionbank(request,id):
    delItem = QuestionBank.objects.get(id=id)
    delpath = "static/media/"+str(delItem.file)
    os.remove(delpath)
    delItem.delete()
    messages.success(request, "Data Delete Successfully")
    return redirect('viewquestionbank')
