
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, City, Village
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
from datetime import datetime
import time
import json
import math
from dss.Serializer import serializer

@csrf_exempt
def admin_device(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_device.html', {})


@csrf_exempt
def admin_device_add(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        city_list = City.objects.all()
        village_list = Village.objects.filter(city=city_list[0])
        return render(request, 'app/admin_deviceAdd.html', {
            "city_list":city_list,
            "village_list":village_list,
        })
    else:
        city_code = request.POST.get("city_code", None)
        get_device_flag = request.POST.get("get_device_flag", None)
        add_user_flag = request.POST.get("add_user_flag", None)
        if get_device_flag is not None:
            pass
        elif add_user_flag is not None:
            pass
        else:
            city_code = int(city_code)
            city  = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
            return HttpResponse(json.dumps(serializer(village_list)), "application/json")
        return HttpResponse("error")


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
    page = request.GET.get("page")
    page_num = int(math.ceil(len(Device.objects.all()) / 10.0))
    print page
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        page = 1
    if page > page_num:
        page = page_num
    start_num = (page - 1) * 10
    end_num = page * 10
    device_list = Device.objects.all().order_by('-id')[start_num:end_num]
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
        "device_list": device_list,
        "page_num": page_num,
        "page" : page,
    })


@csrf_exempt
def instock(request):
    try:
        user = AppUser.objects.get(username = request.session["username"])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        device_type = request.POST.get("type", None)
        device_number = request.POST.get("number", None)
        if device_type is None or device_number is None:
            return HttpResponse("error")
        device_number = int(device_number)
        start_num = 0
        if device_type == "1":
            d_num = Device.objects.filter(device_id__lt=200000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 100000000
            device_type = u"终端"
        elif device_type == "2":
            d_num = Device.objects.filter(device_id__gt=200000000, device_id__lt=300000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 200000000
            device_type = u"中继"
        else:
            d_num = Device.objects.filter(device_id__gt=300000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 300000000
            device_type = u"网关"
        start_no = start_num + 1
        for i in range(device_number):
            start_num += 1
            device = Device()
            device.device_id = start_num
            device.device_status = u"未安装"
            now = time.localtime()
            device.manufacture_date = datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            device.save()
        ret_data = {}
        ret_data["type"] = device_type
        ret_data["start_no"] = start_no
        ret_data["end_no"] = start_num
        return HttpResponse(json.dumps(ret_data), "application/json")
    except Exception, e:
        print str(e)
        return HttpResponse("error")


@csrf_exempt
def device_info(request):
    try:
        user = AppUser.objects.get(username = request.session["username"])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "POST":
        try:
            device_id = request.POST.get('device_id', None)
            print device_id
            if device_id is None:
                return HttpResponse("error")
            device_id = int(device_id)
            device = Device.objects.get(device_id=device_id)
            device.delete()
            return HttpResponse("success")
        except Exception, e:
            print str(e)
            return HttpResponse("error")
    else:
        device_id = int(request.GET("device_id"))

        return HttpResponse("GET")