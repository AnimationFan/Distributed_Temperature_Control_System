from django.shortcuts import render
from django.http import HttpResponse
from UserDefine.ConfigReader import config_info

def show_config(request):
    print(config_info)
    return HttpResponse('Hello')
# Create your views here.
