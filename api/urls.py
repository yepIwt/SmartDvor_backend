from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'api'

urlpatterns = [
    path('', views.welcome, name = 'welcome'),
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('user', views.UserView.as_view()),
    path('user/get', views.UserGetView.as_view()),
    path('users', views.UserListView.as_view()),
    path('posts', views.PostListView.as_view()),
    path('posts/create', views.PostCreateView.as_view()),
    path('comments', views.PostCommentListView.as_view()),
    path('comments/leave', views.PostCommentLeaveView.as_view()),
    path('requests', views.ServiceListView.as_view()),
    path('requests/create', views.ServiceRequestView.as_view()),
    path('requests/my', views.ServiceCustomerListView.as_view()),
]
