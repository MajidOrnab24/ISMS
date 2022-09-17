from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home (request):
    return render(request,'homepage.html' )
def general_login(request):
    return render(request,'general_login.html')
def admission(request):
    return render(request,'admission.html')

