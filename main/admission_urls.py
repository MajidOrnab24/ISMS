from unicodedata import name
from django.urls import path
from main import admission_views as admission_view

urlpatterns = [
    path('login', admission_view.adminLogin, name='login'),
    path('logout', admission_view.adminLogout, name='logout'),
    #path('adminhome',admin_view.adminHome, name='adminhome'),
    path('setroadmap',admission_view.setroadmap, name='setroadmap'),
    path('viewroadmap',admission_view.viewroadmap, name='viewroadmap'),
    path('editroadmap/<str:id>',admission_view.editroadmap, name='editroadmap'),
    path('deleteroadmap/<str:id>',admission_view.deleteroadmap, name='deleteroadmap'),
    path('setfaq',admission_view.setfaq, name='setfaq'),
    path('viewfaq',admission_view.viewfaq, name='viewfaq'),
    path('editfaq/<str:id>',admission_view.editfaq, name='editfaq'),
    path('deletefaq/<str:id>',admission_view.deletefaq, name='deletefaq'),
    path('setquestionbank',admission_view.setquestionbank, name='setquestionbank'),
    path('viewquestionbank',admission_view.viewquestionbank, name='viewquestionbank'),
    path('editquestionbank/<str:id>',admission_view.editquestionbank, name='editquestionbank'),
    path('deletequestionbank/<str:id>',admission_view.deletequestionbank, name='deletequestionbank'),
]




