from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'api'

urlpatterns = [
    path('', views.welcome, name = 'welcome'),
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
]
