# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Adminer, Event
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import time


@csrf_exempt
def admin_index(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    temperature_warning_list = Event.objects.filter(name_no=13).order_by('-time')
    temperature_warning_list = serializer(temperature_warning_list, foreign=True)
    for t in temperature_warning_list:
        t["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t["time"])))
    return render(request, 'app/admin_index.html', {
        "user" : user,
        "temperature_warning_list":temperature_warning_list,
    })


def admin_login(request):
    return render(request, 'app/admin_login.html', {})