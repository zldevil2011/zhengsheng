
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, City, Village, Repairing
from django.contrib.auth.hashers import check_password,make_password
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
    page = int(request.GET.get("page", 1))
    if page < 1:
        return HttpResponseRedirect("/admin_device?page=1")
    try:
        city_code = int(request.GET.get("city_code"))
    except:
        city_code = 0
    try:
        village_code = int(request.GET.get("village_code"))
    except:
        village_code = 0
    print("CV_code:")
    print(city_code)
    print(village_code)
    city_list = City.objects.all()
    try:
        city = City.objects.get(city_code=city_code)
        village_list = Village.objects.filter(city=city)
    except:
        village_list = None
    print("CV:")
    print(city_list)
    print(village_list)

    device_list = Device.objects.exclude(device_status=u"未安装")
    if city_code == 0 and village_code == 0:
        pass
    elif village_code == 0:
        device_list = device_list.filter(city_code=city_code)
    else:
        try:
            device_list = device_list.filter(city_code=city_code, village_code=village_code)
        except:
            pass

    total_page = int(math.ceil(device_list.count()/20.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_device?page=" + str(total_page))
    start_num = (page - 1) * 20
    end_num = page * 20
    device_list = device_list[start_num:end_num]
    device_list = serializer(device_list)
    for device in device_list:
        device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(device["manufacture_date"]))
        D = Device.objects.get(device_id=int(device["device_id"]))
        user = AppUser.objects.get(device=D)
        device["address"] = user.address
        device["user"] = user.username
        print type(device["device_id"])
        if str(device["device_id"])[0:1] == '1':
            device["type"] = u"终端"
        elif str(device["device_id"])[0:1] == '2':
            device["type"] = u"中继"
        else:
            device["type"] = u"网关"
    return render(request, 'app/admin_device.html', {
        "device_list": device_list,
        "page": page,
        "total_page": total_page,
        "city_list": city_list,
        "village_list": village_list,
        "city_code": "c" + str(city_code),
        "village_code": "v" + str(village_code),
    })


@csrf_exempt
def admin_device_filter(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        device_id = request.POST.get("device_id", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)
        key = request.POST.get("key", "")
        print device_id
        print type(start_time)
        print end_time
        print key
        device_list = Device.objects.exclude(device_status=u"未安装")
        if device_id is not None and device_id != "":
            print("ok")
            device_list = device_list.filter(device_id__icontains=device_id)
            device_list = device_list.filter(device_status__icontains=key)
        else:
            device_list = device_list.filter(device_status__icontains=key)
        if start_time is not None and start_time != "":
            start_time = str(start_time) + " 00:00:00"
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            device_list = device_list.filter(manufacture_date__gt=start_time)
        if end_time is not None and end_time != "":
            end_time = str(end_time) + " 23:59:59"
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            device_list = device_list.filter(manufacture_date__lt=end_time)
        print device_list.count()
        device_list = serializer(device_list)
        for device in device_list:
            device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(device["manufacture_date"]))
            D = Device.objects.get(device_id=int(device["device_id"]))
            user = AppUser.objects.get(device=D)
            device["address"] = user.address
            device["user"] = user.username
            print type(device["device_id"])
            if str(device["device_id"])[0:1] == '1':
                device["type"] = u"终端"
            elif str(device["device_id"])[0:1] == '2':
                device["type"] = u"中继"
            else:
                device["type"] = u"网关"
        return HttpResponse(json.dumps(device_list), "application/json")
    except Exception, e:
        print str(e)
        return HttpResponse("error")

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
        print get_device_flag
        print add_user_flag
        if get_device_flag is not None:
            city_code=request.POST.get('city_code')
            village_code=request.POST.get('village_code')
            building_code=request.POST.get('building_code')
            unit_code=request.POST.get('unit_code')
            room_code=request.POST.get('room_code')
            try:
                device = Device.objects.get(city_code=int(city_code), village_code=int(village_code), building_code=int(building_code),
                                            unit_code=int(unit_code), room_code=int(room_code))
                return HttpResponse(device.device_id)
            except Exception, e:
                print str(e)
                return HttpResponse("error")
            pass
        elif add_user_flag is not None:
            print "xyxyxyxyyx"
            try:
                device_id = request.POST.get("device_id", None)
                if device_id is None:
                    return HttpResponse("error")
                device = Device.objects.get(device_id=int(device_id))
                device.device_status = u"正常"
                device.save()
                user = User()
                user.username = request.POST.get('username')
                password = request.POST.get('telephone', '123456')
                password = make_password(password, None, 'pbkdf2_sha256')
                user.password = password
                user.save()
                appuser = AppUser()
                appuser.user = user
                appuser.username = request.POST.get('username','')
                appuser.address = request.POST.get('address','')
                appuser.register_time = datetime.now()
                appuser.telephone = request.POST.get('telephone', '')
                appuser.email = request.POST.get('email', '')
                appuser.password = request.POST.get('telephone', '123456')
                appuser.device = device
                appuser.save()
                return HttpResponse("success")
            except Exception, e:
                print str(e)
                return HttpResponse("error")
        else:
            city_code = int(city_code)
            city  = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
            return HttpResponse(json.dumps(serializer(village_list)), "application/json")
        return HttpResponse("error")


@csrf_exempt
def admin_device_remove(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        if page < 1:
            return HttpResponseRedirect("/admin_device/remove?page=1")
        try:
            city_code = int(request.GET.get("city_code"))
        except:
            city_code = 0
        try:
            village_code = int(request.GET.get("village_code"))
        except:
            village_code = 0
        print("CV_code:")
        print(city_code)
        print(village_code)
        city_list = City.objects.all()
        try:
            city = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
        except:
            village_list = None
        print("CV:")
        print(city_list)
        print(village_list)

        device_list = Device.objects.exclude(device_status=u"未安装")
        if city_code == 0 and village_code == 0:
            pass
        elif village_code == 0:
            device_list = device_list.filter(city_code=city_code)
        else:
            try:
                device_list = device_list.filter(city_code=city_code, village_code=village_code)
            except:
                pass
        # device_list = Device.objects.exclude(device_status=u"未安装")
        total_page = int(math.ceil(device_list.count() / 20.0))
        if total_page < 1:
            total_page = 1
        if page > total_page:
            return HttpResponseRedirect("/admin_device/remove?page=" + str(page))
        start_num = (page - 1) * 20
        end_num = page * 20
        device_list = device_list[start_num:end_num]
        device_list = serializer(device_list)
        for device in device_list:
            device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(device["manufacture_date"]))
            D = Device.objects.get(device_id=int(device["device_id"]))
            user = AppUser.objects.get(device=D)
            device["address"] = user.address
            device["user"] = user.username
            print type(device["device_id"])
            if str(device["device_id"])[0:1] == '1':
                device["type"] = u"终端"
            elif str(device["device_id"])[0:1] == '2':
                device["type"] = u"中继"
            else:
                device["type"] = u"网关"

        return render(request, 'app/admin_deviceRemove.html', {
            "device_list": device_list,
            "page": page,
            "total_page": total_page,
            "city_list": city_list,
            "village_list": village_list,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
        })
    else:
        device_id = request.POST.get("device_id", None)
        if device_id is None:
            return HttpResponse("error")
        try:
            device_id = int(device_id)
            device = Device.objects.get(device_id = device_id)
            appuser = AppUser.objects.get(device=device)
            appuser.device = None
            appuser.save()
            device.device_status = u"未安装"
            device.save()
            return HttpResponse("success")
        except Exception, e:
            print str(e)
            return HttpResponse("error")


def admin_device_location(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_deviceLocation.html', {})


@csrf_exempt
def admin_device_maintain(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        try:
            city_code = int(request.GET.get("city_code"))
        except:
            city_code = 0
        try:
            village_code = int(request.GET.get("village_code"))
        except:
            village_code = 0
        print("CV_code:")
        print(city_code)
        print(village_code)
        city_list = City.objects.all()
        try:
            city = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
        except:
            village_list = None
        print("CV:")
        print(city_list)
        print(village_list)

        repair_list = Repairing.objects.all().order_by('-time')
        if city_code == 0 and village_code == 0:
            pass
        elif village_code == 0:
            device_list = repair_list.filter(device__city_code=city_code)
        else:
            try:
                device_list = repair_list.filter(device__city_code=city_code, device__village_code=village_code)
            except:
                pass
        page = int(request.GET.get("page", 1))
        if page < 1:
            return HttpResponseRedirect("/admin_device/maintain?page=1")
        # repair_list = Repairing.objects.all().order_by('-time')
        total_page = int(math.ceil(repair_list.count()/10.0))
        if total_page < 1:
            total_page = 1
        if page > total_page:
            return HttpResponseRedirect("/admin_device/maintain?page=" + str(total_page))
        start_num = (page - 1) * 20
        end_num = page * 20
        repair_list = repair_list[start_num:end_num]
        repair_list = serializer(repair_list, foreign=True)
        for repair in repair_list:
            device = Device.objects.get(device_id=int(repair["device"]["device_id"]))
            if str(device.device_id)[0:1] == '1':
                repair["type"] = u"终端"
            elif str(device.device_id)[0:1] == '2':
                repair["type"] = u"中继"
            else:
                repair["type"] = u"网关"
            repair["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(repair["time"])))
            appuser = AppUser.objects.get(device=device)
            repair["address"] = appuser.address
            repair["user"] = appuser.username

        return render(request, 'app/admin_deviceMaintain.html', {
            "repair_list": repair_list,
            "page": page,
            "total_page": total_page,
            "city_list": city_list,
            "village_list": village_list,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
        })
    else:
        repair_id = request.POST.get("repair_id", None)
        if repair_id is None:
            return HttpResponse("error")
        repair_id = int(repair_id)
        try:
            repair = Repairing.objects.get(id = repair_id)
            device = repair.device
            user = AppUser.objects.get(device=device)
            repair = serializer(repair)
            if str(device.device_id)[0:1] == '1':
                repair["type"] = u"终端"
            elif str(device.device_id)[0:1] == '2':
                repair["type"] = u"中继"
            else:
                repair["type"] = u"网关"
            repair["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(repair["time"])))
            repair["user"] = user.username
            return HttpResponse(json.dumps(repair), "application/json")
        except Exception, e:
            print str(e)
            return HttpResponse("error")


@csrf_exempt
def admin_device_maintain_filter(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        device_id = request.POST.get("device_id", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)
        key = request.POST.get("key", "")
        print device_id
        print type(start_time)
        print end_time
        print key
        device_list = Repairing.objects.all().order_by('-time')
        if device_id is not None and device_id != "":
            print("ok")
            device_list = device_list.filter(device__device_id__icontains=device_id)
            device_list = device_list.filter(device__device_status__icontains=key)
        else:
            device_list = device_list.filter(device__device_status__icontains=key)
        if start_time is not None and start_time != "":
            start_time = str(start_time) + " 00:00:00"
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            device_list = device_list.filter(time__gt=start_time)
        if end_time is not None and end_time != "":
            end_time = str(end_time) + " 23:59:59"
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            device_list = device_list.filter(time__lt=end_time)
        print device_list.count()
        device_list = serializer(device_list, foreign=True)
        for device in device_list:
            device["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(device["time"]))
            D = Device.objects.get(device_id=int(device["device"]["device_id"]))
            user = AppUser.objects.get(device=D)
            device["address"] = user.address
            device["user"] = user.username
            print type(device["device_id"])
            if str(device["device"]["device_id"])[0:1] == '1':
                device["type"] = u"终端"
            elif str(device["device"]["device_id"])[0:1] == '2':
                device["type"] = u"中继"
            else:
                device["type"] = u"网关"
        return HttpResponse(json.dumps(device_list), "application/json")
    except Exception, e:
        print str(e)
        return HttpResponse("error")


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
        start_num = int(start_num)
        start_num += 1
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
        ret_data["start_no"] = start_num
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