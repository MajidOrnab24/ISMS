import email
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import UserAccount
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.


def home (request):
    return render(request,'homepage.html' )
def general_login(request):
    return render(request,'general_login.html')
def admission(request):
    return render(request,'admission.html')
def signout(request):
     return render(request,'signout.html')
def signup(request):
     return render(request,'signup.html')

def signin(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


