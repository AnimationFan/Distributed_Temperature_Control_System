from django.urls import path
from 温控系统 import views

urlpatterns=[
    path('conifg/',views.show_config),
    path('init/',views.init),
    path('add/',views.addair),
    path('del/',views.delair),
    path('Login/', views.login),
    path('logout/', views.logout),
    path('setPassWord/', views.setPassWord),
    path('writesession/', views.writesession),
    path('readsession/', views.readsession),
    path('decoratortest/',views.test_decoratort),
    path(r'', views.welcome),

]

