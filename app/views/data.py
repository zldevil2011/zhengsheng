
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, City, Village
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import time
import math


@csrf_exempt
def admin_data(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    page = int(request.GET.get("page", 1))
    if page < 1:
        return HttpResponseRedirect("/admin_data?page=1")
    start_num = (page - 1) * 10
    end_num = (page) * 10
    city_code = 32701
    village_code = 10001
    city = City.objects.get(city_code=city_code)
    village = Village.objects.get(village_code=village_code)
    # 首先查找出属于该地区的所有终端
    device_list = Device.objects.filter(city_code=city_code, village_code=village_code)
    total_page = int(math.ceil(device_list.count()/10.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_data?page=" + str(total_page))
    device_list = device_list[start_num:end_num]
    device_list = serializer(device_list)
    for device in device_list:
        address = city.city_name + village.village_name
        device["address"] = address
        if str(device["device_id"])[0:1] == "1":
            device["type"] = u"终端"
        elif str(device["device_id"])[0:1] == "2":
            device["type"] = u"中继"
        else:
            device["type"] = u"网关"
        device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["manufacture_date"])))

    return render(request, 'app/admin_data.html', {
        "device_list": device_list,
        "page": page,
        "total_page": total_page,
    })


