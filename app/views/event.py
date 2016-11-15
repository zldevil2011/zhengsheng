# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, City, Village, Adminer, Event
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import time
import math
from datetime import datetime, date, timedelta
import sys
import json
from django.core.mail import send_mail
from zhengsheng import settings

@csrf_exempt
def admin_event(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    event_list = Event.objects.all()
    total_page = int(math.ceil(event_list.count() / 10.0))
    if total_page < 1:
        total_page = 1
    if page < 1:
        return HttpResponseRedirect("/admin_event?page=1")
    if page > total_page:
        return HttpResponseRedirect("/admin_event?page=" + str(total_page))
    start_num = (page - 1) * 10
    end_num = page * 10
    event_list = event_list[start_num:end_num]
    event_list = serializer(event_list, foreign=True)
    for event in event_list:
        event["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event["time"]))
    return render(request, 'app/admin_event.html', {
        "event_list": event_list,
        "page": page,
        "total_page": total_page,
        "user": user,
    })


@csrf_exempt
def user_send_mail(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        event_id = int(request.POST.get("event_id"))
        event = Event.objects.get(id=event_id)
        subject = u"事件通知"
        text_content = u"您的设备（ID:" + str(event.device.device_id) + u")在" + str(event.time) + u"发生了" + str(event.name) + u"事件，请您及时查看或联系供电公司"
        from_email = settings.EMAIL_HOST_USER
        appuser = AppUser.objects.get(device=event.device)
        to = appuser.email
        try:
            send_mail(subject, text_content, from_email, [to], fail_silently=False)
            return HttpResponse("success")
        except Exception as e:
            print "level1"
            print(str(e))
            return HttpResponse("error")
    except Exception, e:
        print "level2"
        print(str(e))
        return HttpResponse("error")
