from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('general login',views.general_login, name='general_login'),
    path('admission',views.admission, name='admission'),
    path('signin',views.signin, name='signin'),

    ]