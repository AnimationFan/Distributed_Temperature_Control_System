from django.urls import path
from 温控系统 import views

urlpatterns=[
    path('conifg', views.show_config),
    path('init', views.init),
    path('login', views.login),
    path('logout', views.logout),
    path('setPassWord', views.setPassWord)
]
