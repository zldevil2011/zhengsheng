
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
from datetime import datetime
import time

@csrf_exempt
def admin_device(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_device.html', {})


def admin_device_add(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        return render(request, 'app/admin_deviceAdd.html', {})
    else:
        return HttpResponse("POST")


def admin_device_remove(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        return render(request, 'app/admin_deviceRemove.html', {})
    else:
        return HttpResponse("POST")


def admin_device_location(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_deviceLocation.html', {})


def admin_device_maintain(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_deviceMaintain.html', {})


def admin_device_temperature(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_temperature.html', {})


def admin_device_health(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_deviceHealth.html', {})


def admin_device_leakage(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_leakage.html', {})


def list(request):
    try:
        user = AppUser.objects.get(username = request.session["username"])
    except:
        return HttpResponseRedirect("/admin_login/")
    page = int(request.POST.get("page", 1))
    start_num = (page - 1) * 20
    end_num = page * 20
    device_list = Device.objects.all().order_by('manufacture_date')[start_num:end_num]
    device_list = serializer(device_list)
    for device in device_list:
        device_id = str(device["device_id"])
        if device_id[0] == '1':
            device["type"] = u"终端"
        elif device_id[0] == '2':
            device["type"] = u"中继"
        else:
            device["type"] = u"网关"
        str_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(int(device["manufacture_date"])))
        device["manufacture_date"] = str_time
    print device_list
    return render(request, "app/device_list.html", {
       "device_list": device_list
    })

