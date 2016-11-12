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

