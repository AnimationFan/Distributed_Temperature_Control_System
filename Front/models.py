from django.db import models
from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail

# -*- coding: UTF-8 -*-

user_list = [
]

prepage = 1

page_list = [
]

guan_list = [
]

username = "h"
password = "p"
weiboid = 1

cap = 1000
acc = "1"

def Login(request):
    return render_to_response('Login.html')

@csrf_exempt
def search(request):
    global guan_list
    list = models.User.objects.all()

    data2 = models.Weibo.objects.all()
    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in data2:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z
        x.save()

    data2 = models.Weibo.objects.filter(page=prepage)

    global username
    username = request.GET['name']
    global password
    password = request.GET['password']
    for var in list:
        if var.name == username and var.password == password:
            data = var.name
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            guan_list = models.FocusList.objects.filter(belong_id=var.id)
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})
    return render_to_response('Login.html')


@csrf_exempt
def NewUser(request):
    if request.method == 'GET':
        return render_to_response('NewUser.html')
    if request.method == 'POST':
        n = request.POST.get('name')
        p = request.POST.get('password')
        e = request.POST.get('Email')
        prelist1 = models.User.objects.filter(name=n)
        prelist2 = models.User.objects.filter(Email=e)
        if prelist1.count() == 0 and prelist2.count() == 0:
            list = models.User(name=n, password=p, Email=e)
            list.save()
            return render_to_response('Login.html')
    return render_to_response('NewUser.html')


def Go(request):
    global guan_list
    a = request.GET['id']
    b = int(a)
    c = models.Weibo.objects.get(id=b)
    c.zan = c.zan + 1
    global weiboid
    weiboid = c.id
    c.save()
    list = models.Weibo.objects.all()
    r_list = models.Comment.objects.filter(belong_id=b)
    for var in list:
        if var.id == b:
            data = var
            return render(request, 'blog.html', {'data': data, "posts": r_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


@csrf_exempt
def Fo(request):
    global guan_list
    a = request.GET['name']
    b = request.GET['id']
    c = request.GET['if']
    f = request.GET['wid']
    list = models.User.objects.all()
    d = 0

    for var in list:
        if var.name == b:
            d = var.id
    if c == "关注":
        m = models.FocusList(name=a, belong_id=d)
        m.save()
    if c == "已关注":
        m = models.FocusList.objects.get(name=a, belong_id=d)
        m.delete()
    if c == "编辑":
        global weiboid
        weiboid = int(f)
        e = models.Weibo.objects.get(id=f).content
        return render(request, 'editblog.html', {'data': b, "posts": e, 'guanzhu': guan_list})

    for var in list:
        if var.name == b:
            data = var.name
            data2 = models.Weibo.objects.filter(page=prepage)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()

            guan_list = models.FocusList.objects.filter(belong_id=var.id)
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})
    return render_to_response('blogindex.html')


def Plist(request):
    global guan_list
    a = request.GET['id']
    list = models.Weibo.objects.order_by("-commentNum")
    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in list:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z
    data2 = list.filter(page=prepage)
    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            data = var.name
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})
    return render_to_response('blogindex.html')


def Zlist(request):
    global guan_list
    a = request.GET['id']
    list = models.Weibo.objects.order_by("-zan")
    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in list:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z
    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            data = var.name
            data2 = list.filter(page=prepage)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": list, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


def NewBlog(request):
    global guan_list
    a = request.GET['id']
    list = models.User.objects.all()
    for var in list:
        if var.name == a:
            data = var.name
            return render(request, 'newblog.html', {'data': data, 'guanzhu': guan_list})


@csrf_exempt
def WriteBlog(request):
    global guan_list
    a = username
    b = request.POST.get('weibo')
    c = request.POST.get('huati')

    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            newWei = models.Weibo(content=b, belong_id=var.id, belong_name=a, zan=0, commentNum=0, ifGuanzhu="关注",
                                  topic=c)
            newWei.save()

    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in models.Weibo.objects.all():
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z

    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.filter(page=prepage)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


def NewComment(request):
    global guan_list
    a = username
    b = request.POST.get('message')
    c = models.Weibo.objects.get(id=weiboid)
    c.commentNum = c.commentNum + 1
    c.save()
    newhui = models.Comment(content=b, belong_id=weiboid, belong_name=a)
    newhui.save()
    r_list = models.Comment.objects.filter(belong_id=weiboid)
    return render(request, 'blog.html', {'data': c, "posts": r_list, 'guanzhu': guan_list})


def Back(request):
    global guan_list
    a = request.GET['id']
    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.all()

            page_list.clear()
            page_list.append(1);
            y = 0
            z = 1
            for x in data2:
                y = y + 1
                if y == 5:
                    y = 1
                    z = z + 1
                    page_list.append(z);
                x.page = z
            data2 = models.Weibo.objects.filter(page=prepage)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


@csrf_exempt
def MyBlog(request):
    global guan_list
    a = request.GET['id']
    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.filter(belong_name=a)
            data3 = models.FocusList.objects.all()

            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html', {'data': data, "posts": data2, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


def EditBlog(request):
    global guan_list
    a = username
    b = request.POST.get('weibo')
    c = request.POST.get('huati')
    list2 = models.User.objects.all()
    newWei = models.Weibo.objects.get(id=weiboid)
    newWei.content = b
    newWei.topic = c;
    newWei.save()

    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in models.Weibo.objects.all():
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z

    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.filter(page=1)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


@csrf_exempt
def top(request):
    global guan_list
    a = request.GET['id']
    b = request.GET['topic']
    list = models.Weibo.objects.filter(topic=b)
    list2 = models.User.objects.all()

    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in list:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z

    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.all()
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": list, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


@csrf_exempt
def Sousuo(request):
    global guan_list
    global username
    a = username
    b = request.POST.get('q')

    list3 = models.Weibo.objects.all()
    if list3.filter(belong_name=b).count() != 0:
        list = models.Weibo.objects.filter(belong_name=b)

    else:
        list = models.Weibo.objects.filter(topic=b)

    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in list:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z

    list2 = models.User.objects.all()
    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.all()
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": list, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


def tracepwd_link(request):
    return render(request, "tracepwd.html")


@csrf_exempt
def tracepwd(request):
    global cap
    global acc
    import random
    cap = random.randint(1000, 9999)
    cap = str(cap)
    traceemail = request.POST.get('email')
    if traceemail != "":
        traceacc = models.User.objects.filter(Email=traceemail)
        if traceacc.count() != 0:
            aa = models.User.objects.get(Email=traceemail)
            acc = aa.Email
            msg = '用户您好！\n        您收到这封邮件是因为您请求找回在网站 127.0.0.1:8000上的用户账户密码。\n        您的验证码为：' + cap
            send_mail('找回密码',
                      msg,
                      settings.EMAIL_FROM,
                      [traceemail]
                      , fail_silently=False, )
            return render(request, "showpwd.html")
    return render(request, "tracepwd.html")


@csrf_exempt
def showpwd(request):
    global cap
    getcap = request.POST.get('cap')
    if cap == getcap:
        aa = models.User.objects.filter(Email=acc)
        return render(request, "showpwd2.html", {"data": aa})
    return render(request, "showpwd.html")


@csrf_exempt
def Page(request):
    global guan_list
    global username
    a = username
    b = request.GET['page']
    global prepage
    prepage = b
    list = models.Weibo.objects.filter(page=prepage)
    list2 = models.User.objects.all()

    data2 = models.Weibo.objects.all()
    page_list.clear()
    page_list.append(1);
    y = 0
    z = 1
    for x in data2:
        y = y + 1
        if y == 5:
            y = 1
            z = z + 1
            page_list.append(z);
        x.page = z

    for var in list2:
        if var.name == a:
            data = var.name
            data2 = models.Weibo.objects.all()
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": list, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')


def Home(request):
    global guan_list
    list2 = models.User.objects.all()
    for var in list2:
        if var.name == username:
            data = var.name
            data2 = models.Weibo.objects.filter(page=1)
            data3 = models.FocusList.objects.all()
            for var2 in data2:
                if data == var2.belong_name:
                    var2.ifGuanzhu = "编辑"
                    var2.save()
                else:
                    if data3.filter(belong_id=var.id).count() != 0:
                        data4 = data3.filter(belong_id=var.id)
                        if data4.filter(name=var2.belong_name).count() != 0:
                            var2.ifGuanzhu = "已关注"
                            var2.save()
                        else:
                            var2.ifGuanzhu = "关注"
                            var2.save()
                    else:
                        var2.ifGuanzhu = "关注"
                        var2.save()
            return render(request, 'blogindex.html',
                          {'data': data, "posts": data2, 'pages': page_list, 'guanzhu': guan_list})

    return render_to_response('blogindex.html')

