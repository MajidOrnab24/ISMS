from unicodedata import name
from django.urls import path
from . import views
from main import studentViews as student_view
from main import admission_views as admissionView
from admin_app import views as admin_view

urlpatterns = [
    path('',views.home, name='home'),
    path('general login',views.general_login, name='general_login'),
    # Admission urls
    path('admission',admissionView.admission, name='admission'),
    path('about',admissionView.about, name='about'),
    path('faq',admissionView.faq, name='faq'),
    path('questionBank',admissionView.questionBank, name='questionBank'),
    path('roadMap',admissionView.roadMap, name='roadMap'),




    # Login urls
    path('signinStudent',views.signinStudent, name='signinStudent'),
    path('signinFaculty',views.signinFaculty, name='signinFaculty'),
    path('signinStaff',views.signinStaff, name='signinStaff'),
    path('logout',views.logout_request, name='logout'),
    path('logError',views.logError, name='logError'),
    # student urls
    path('studentPage',student_view.studentPage, name='studentPage'),










    # faculty urls
    path('facultyPage',views.facultyPage, name='facultyPage'),










    # Med staff urls
    path('staffMedPage',views.staffMedPage, name='staffMedPage'),








    # Lib staff urls
    path('staffLibPage',views.staffLibPage, name='staffLibPage'),







    # admin urls 
    path('adminHome',admin_view.adminHome,name='adminHome'),
    path('adminStudent',admin_view.adminStudent,name='adminStudent'),
    path('studentregister',admin_view.studentregister,name='studentregister'),
    path('deleteStudent/<int:id>', admin_view.deleteStudent, name='deleteStudent'),
    path('studentUpdate/<int:id>', admin_view.studentUpdate, name='studentUpdate'),
    path('facultyregister',admin_view.facultyregister,name='facultyregister'),
    path('adminFaculty',admin_view.adminFaculty,name='adminFaculty'),
    path('deleteFaculty/<int:id>', admin_view.deleteFaculty, name='deleteFaculty'),

    ]