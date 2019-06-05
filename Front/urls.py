from django.conf.urls import url
from django.contrib import admin
from Front import views

urlpatterns = [
    url('login', views.login),
    url('getAccount', views.getAccount),
    url('logout', views.logout),
    url('', views.welcome),
]