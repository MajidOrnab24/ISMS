from unicodedata import name
from django.urls import path
from . import views
from main import studentViews as student_view

from unicodedata import name
from django.urls import path
from . import views
from admin_app import views as admin_view

urlpatterns = [
    path('',views.home, name='home'),
    path('general login',views.general_login, name='general_login'),


    # Admission urls
    path('admission',views.admission, name='admission'),
    path('about',views.about, name='about'),
    path('faq',views.faq, name='faq'),
    path('questionBank',views.questionBank, name='questionBank'),
    path('roadMap',views.roadMap, name='roadMap'),


    # Admission urls of admin
    path('admin_roadmap',admin_view.admin_roadmap,name='admin_roadmap'),
    path('roadmap_add',admin_view.roadmap_add,name='roadmap_add'),
    path('delete_roadmap/<int:id>', admin_view.delete_roadmap, name='delete_roadmap'),
    path('update_roadmap/<int:id>', admin_view.update_roadmap, name='update_roadmap'),
    path('admin_faq',admin_view.admin_faq,name='admin_faq'),
    path('faq_add',admin_view.faq_add,name='faq_add'),
    path('delete_faq/<int:id>', admin_view.delete_faq, name='delete_faq'),
    path('update_faq/<int:id>', admin_view.update_faq, name='update_faq'),





    # Login urls
    path('signinStudent',views.signinStudent, name='signinStudent'),
    path('signinFaculty',views.signinFaculty, name='signinFaculty'),
    path('signinStaff',views.signinStaff, name='signinStaff'),
    path('logout',views.logout_request, name='logout'),
    path('logError',views.logError, name='logError'),


    # student urls
    path('studentPage',student_view.studentPage, name='studentPage'),
    path('changePasswordStudent',student_view.changePasswordStudent, name='changePasswordStudent'),










    # faculty urls
    path('facultyPage',views.facultyPage, name='facultyPage'),










    # Med staff urls
    path('staffMedPage',views.staffMedPage, name='staffMedPage'),








    # Lib staff urls
    path('staffLibPage',views.staffLibPage, name='staffLibPage'),







    # admin urls 
    path('adminHome',admin_view.adminHome,name='adminHome'),

    # Admin Students urls
    path('adminStudent',admin_view.adminStudent,name='adminStudent'),
    path('studentregister',admin_view.studentregister,name='studentregister'),
    path('deleteStudent/<int:id>', admin_view.deleteStudent, name='deleteStudent'),
    path('studentUpdate/<int:id>', admin_view.studentUpdate, name='studentUpdate'),
    path('studentChangePass/<int:id>', admin_view.studentChangePass, name='studentChangePass'),

    # Admin Faculty urls
    path('adminFaculty',admin_view.adminFaculty,name='adminFaculty'),
    path('facultyregister',admin_view.facultyregister,name='facultyregister'),
    path('deleteFaculty/<int:id>', admin_view.deleteFaculty, name='deleteFaculty'),
    path('facultyUpdate/<int:id>', admin_view.facultyUpdate, name='facultyUpdate'),
    path('facultyChangePass/<int:id>', admin_view.facultyChangePass, name='facultyChangePass'),

    # Admin Medical Staff urls
    path('adminStaff_med',admin_view.adminStaff_med,name='adminStaff_med'),
    path('staff_med_register',admin_view.staff_med_register,name='staff_med_register'),
    path('deleteStaffMed/<int:id>', admin_view.deleteStaffMed, name='deleteStaffMed'),
    path('staff_medChangePass/<int:id>', admin_view.staff_medChangePass, name='staff_medChangePass'),
    path('staff_medUpdate/<int:id>', admin_view.staff_medUpdate, name='staff_medUpdate'),

    # Admin Library Staff urls
    path('adminStaff_lib',admin_view.adminStaff_lib,name='adminStaff_lib'),
    path('staff_lib_register',admin_view.staff_lib_register,name='staff_lib_register'),
    path('staff_libUpdate/<int:id>', admin_view.staff_libUpdate, name='staff_libUpdate'),
    path('deleteStaffLib/<int:id>', admin_view.deleteStaffLib, name='deleteStaffLib'),
    path('staff_libChangePass/<int:id>', admin_view.staff_libChangePass, name='staff_libChangePass'),

    ]