
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Adminer
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime
import time
from dss.Serializer import serializer
import math
from django.core.mail import send_mail
from zhengsheng import settings

@csrf_exempt
def user(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        try:
            page = int(request.GET.get("page"))
        except:
            page = 1
        if page < 1:
            return HttpResponseRedirect("/admin_info/user/?page=1")
        start_num = (page - 1) * 15
        end_num = (page) * 15
        adminer_list = Adminer.objects.all()
        page_num = int(math.ceil(len(adminer_list)/15.0))
        if page_num < 1:
            page_num = 1
        if page > page_num:
            return HttpResponseRedirect("/admin_info/user?page=" + str(page_num))
        adminer_list = adminer_list[start_num:end_num]
        adminer_list = serializer(adminer_list)
        for adminer in adminer_list:
            adminer["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(adminer["time"]))
        print adminer_list
        return render(request, 'app/admin_admin_list.html', {
            "user": user,
            "adminer_list": adminer_list,
            "page": page,
            "total_page": page_num,
        })
    else:
        try:
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            area = request.POST.get("area")
            try:
                adminer = Adminer.objects.get(name=name)
                return HttpResponse("error")
            except:
                pass
            adminer = Adminer()
            adminer.name = name
            adminer.telephone = phone
            adminer.area = area
            adminer.email = email
            user = User()
            user.username = name
            password = request.POST.get('phone', '123456')
            password = make_password(phone, None, 'pbkdf2_sha256')
            user.password = password
            user.save()
            adminer.user = user
            adminer.save()
            return HttpResponse("success")
        except:
            return HttpResponse("error")


@csrf_exempt
def sendMail(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        text_content = request.POST.get("content")
        from_email = settings.EMAIL_HOST_USER
        to = email

        try:
            send_mail(subject, text_content, from_email, [to], fail_silently=False)
            return HttpResponse("success")
        except Exception as e:
            print(str(e))
            return HttpResponse("error")
    except Exception, e:
        print(str(e))
        return HttpResponse("error")