from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from UserDefine.ConfigReader import config_info
from 温控系统.models import User,AirC

def show_config(request):
    print(config_info)
    for airc in AirC.objects.all():
        print(airc.room_num)
    return HttpResponse('Hello')
# Create your views here.

