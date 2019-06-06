from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import 温控系统.models
class SessionCheck:
    def writeSession(request,user_name:str,password:str,type:str):
        request.session["user_name"]=user_name
        request.session["password"]=password
        request.session["type"]=type
        return True

    def readSession(request):
        result={"user_name":"","password":"","type":""}
        result["user_name"]=request.session["user_name"]
        result["password"]=request.session["password"]
        result["type"]=request.session["type"]
        return result

    def checkSession(request):
        user_name=request.session["user_name"]
        password=request.session["password"]
        type=request.session["type"]
        count=温控系统.models.User.objects.filter(user_name=user_name,password=password,user_type=type).count()
        if count==0:
            return False
        else:
            return True
