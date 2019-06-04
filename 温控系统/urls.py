from django.urls import path
from 温控系统 import views

urlpatterns=[
    path('conifg',views.show_config),
    path('init',views.init),
    path('',views.login)
]