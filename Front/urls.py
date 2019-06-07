from django.urls import path
from django.contrib import admin
from Front import views

urlpatterns = [
    path('login/', views.login),
    path('getAccount/', views.getAccount),
    path('logout/', views.logout),
    path('viewlogin/', views.viewlogin),#录入信息
    path('viewlogout/', views.viewlogout),
    path(r'', views.welcome),
]