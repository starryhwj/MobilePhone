# -*- coding: utf-8 -*-
# filename: Users/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword')
]
