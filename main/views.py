import email
from email.message import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from main.forms import *
import random

# Create your views here.


def home (request):
    return render(request,'homepage.html' )
def general_login(request):
    return render(request,'general_login.html')
def admission(request):
    return render(request,'admission.html')
def signup(request):
    return render(request,'signup.html')
def signout(request):
    return render(request,'signout.html')
# student page views
def studentPage(request):
    return render(request,'studentPage.html')

def signin(request):
    form = signinform(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserAccount = authenticate(email=email, password=password)
            if User is not None :
                login(request, UserAccount)
                return redirect('studentPage')
                
            else:
                msg= 'invalid credentials'
                return redirect('signin')
        else:
            msg = 'error validating form'
    return render(request, 'signin.html', {'form': form, 'msg': msg})
    
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     user = auth.authenticate(email=email, password=password)

    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect('/')
    #     else:
    #         messages.info(request, 'Credentials Invalid')
    #         return redirect('signin')

    # else:
    #     return render(request, 'signin.html')


