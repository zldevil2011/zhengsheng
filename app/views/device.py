
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, City, Village, Repairing, Adminer, Parameter, Data, Relay
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
        user = Adminer.objects.get(name=request.session['username'])
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
        user_t = AppUser.objects.get(device=D)
        try:
            city_t = City.objects.get(city_code=int(D.city_code))
            village_t = Village.objects.get(city=city_t, village_code=int(D.village_code))
            address = city_t.city_name + village_t.village_name
        except:
            address = user_t.address
        device["address"] = address
        device["user"] = user_t.username
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
        "user": user,
    })


@csrf_exempt
def admin_device_filter(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
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
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        city_list = City.objects.all()
        village_list = Village.objects.filter(city=city_list[0])
        return render(request, 'app/admin_deviceAdd.html', {
            "city_list":city_list,
            "village_list":village_list,
            "user": user,
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
                try:
                    # 如果设备对应的用户存在，则对用户信息进行更新
                    appuser = AppUser.objects.get(device=device)
                    user = appuser.user
                    user.username = request.POST.get('username').strip()
                    password = request.POST.get('telephone', '123456').strip()
                    if len(password) == 0:
                        password = '123456'
                    print "password", password
                    secret_password = make_password(password, None, 'pbkdf2_sha256')
                    user.password = secret_password
                    user.save()
                    appuser.username = request.POST.get('username').strip()
                    appuser.address = request.POST.get('address', '').strip()
                    appuser.register_time = datetime.now()
                    appuser.telephone = request.POST.get('telephone', '').strip()
                    appuser.email = request.POST.get('email', '').strip()
                    appuser.password = password
                    appuser.save()
                except:
                    # 否则则创建新的用户
                    user = User()
                    user.username = request.POST.get('username').strip()
                    password = request.POST.get('telephone', '123456').strip()
                    if len(password) == 0:
                        password = '123456'
                    secret_password = make_password(password, None, 'pbkdf2_sha256')
                    user.password = secret_password
                    user.save()
                    appuser = AppUser()
                    appuser.user = user
                    appuser.username = request.POST.get('username').strip()
                    appuser.address = request.POST.get('address','').strip()
                    appuser.register_time = datetime.now()
                    appuser.telephone = request.POST.get('telephone', '').strip()
                    appuser.email = request.POST.get('email', '').strip()
                    appuser.password = password
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
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    print(request.session['username'])
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
            user_t = AppUser.objects.get(device=D)
            device["address"] = user_t.address
            device["user"] = user_t.username
            print type(device["device_id"])
            if str(device["device_id"])[0:1] == '1':
                device["type"] = u"终端"
            elif str(device["device_id"])[0:1] == '2':
                device["type"] = u"中继"
            else:
                device["type"] = u"网关"
        print "device remove - user = ", user
        return render(request, 'app/admin_deviceRemove.html', {
            "device_list": device_list,
            "page": page,
            "total_page": total_page,
            "city_list": city_list,
            "village_list": village_list,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
            "user": user,
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
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_deviceLocation.html', {
        "user": user,
    })


@csrf_exempt
def admin_device_maintain(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
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
            "user": user,
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
        user = Adminer.objects.get(name=request.session['username'])
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


@csrf_exempt
def admin_device_temperature(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        try:
            page = int(request.GET.get("page"))
        except Exception, e:
            print(str(e))
            page = 1
        print "page=", page
        if page < 1:
            print "okokoko"
            return HttpResponseRedirect("/admin_device/temperature/?page=1")
        city_code = int(request.GET.get("city_code", 0))
        village_code = int(request.GET.get("village_code", 0))

        city_list = City.objects.all()
        try:
            city = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
        except:
            village_list = None

        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        # print today
        device_list = Device.objects.exclude(device_status=u"未安装")
        try:
            if city_code == 0 and village_code == 0:
                pass
            elif village_code == 0:
                device_list = device_list.filter(city_code=city_code)
            else:
                try:
                    device_list = device_list.filter(city_code=city_code, village_code=village_code)
                except:
                    pass
        except:
            pass
        total_page = int(math.ceil(len(device_list)/15.0))
        if total_page < 1:
            total_page = 1
        if page > total_page:
            return HttpResponseRedirect("/admin_device/temperature/?page="+str(total_page))
        start_num = (page - 1) * 15
        end_num = page * 15
        device_list = device_list[start_num:end_num]
        device_list = serializer(device_list, foreign=True)
        for device in device_list:
            try:
                city = City.objects.get(city_code=int(device["city_code"]))
                village = Village.objects.get(city=city, village_code=int(device["village_code"]))
                city_name = city.city_name
                village_name = village.village_name
                address = city_name + village_name
            except:
                address = ""
            try:
                device_tmp = Device.objects.get(device_id=int(device["device_id"]))
                user_new = AppUser.objects.get(device=device_tmp).username
            except:
                user_new = ""
            try:
                manufacture_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["manufacture_date"])))
            except:
                manufacture_date = ""
            try:
                device_tmp = Device.objects.get(device_id=int(device["device_id"]))
                temperature = Data.objects.filter(device_id=device_tmp).order_by('-tempT')[0].temp
                temperature_time = str(Data.objects.filter(device_id=device_tmp).order_by('-tempT')[0].tempT)
            except:
                temperature = u"未监测到"
                temperature_time = u"未监测到"
            device["address"] = address
            device["user"] = user_new
            device["manufacture_date"] = manufacture_date
            device["temperature"] = temperature
            device["temperature_time"] = temperature_time

        print(device_list)
        return render(request, 'app/admin_temperature.html', {
            "device_list": device_list,
            "user": user,
            "page": page,
            "total_page": total_page,
            "city_list": city_list,
            "village_list": village_list,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
        })
    else:
        try:
            device_id = int(request.POST.get("device_id"))
            device = Device.objects.get(device_id=device_id)
            try:
                start_time = request.POST.get("start_time")
                end_time = request.POST.get("end_time")
                start_time = datetime.strptime(start_time, "%Y-%m-%d")
                end_time = datetime.strptime(end_time, "%Y-%m-%d")
            except Exception as e:
                print(str(e))
                today = datetime.today()
                start_time = datetime(today.year, today.month, today.day)
                end_time = datetime(today.year, today.month, today.day) + timedelta(days=1)
            print(start_time)
            print(end_time)
            data_list = Data.objects.filter(tempT__gte=start_time, tempT__lte=end_time, device_id=device).order_by('tempT')
            today_temp = []
            today_hour = []
            for d in data_list:
                if d.temp is not None:
                    today_temp.append(d.temp)
                    today_hour.append(str(d.tempT))
            today_data = {}
            today_data["today_temp"] = today_temp
            today_data["today_hour"] = today_hour
            print today_data
            return HttpResponse(json.dumps(today_data), "application/json")
        except:
            return HttpResponse("error")


def admin_device_health(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    # 查看高温报警（今日数据） / 故障检测待定
    try:
        page = int(request.GET.get("page"))
    except Exception, e:
        print(str(e))
        page = 1
    print "page=", page
    if page < 1:
        print "okokoko"
        return HttpResponseRedirect("/admin_device/health/?page=1")
    city_code = int(request.GET.get("city_code", 0))
    village_code = int(request.GET.get("village_code", 0))

    city_list = City.objects.all()
    try:
        city = City.objects.get(city_code=city_code)
        village_list = Village.objects.filter(city=city)
    except:
        village_list = None

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    print today
    device_list = Data.objects.filter().order_by('-date_time')
    try:
        if city_code == 0 and village_code == 0:
            pass
        elif village_code == 0:
            device_list = device_list.filter(device_id__city_code=city_code)
        elif city_code != 0 and village_code != 0:
            device_list = device_list.filter(device_id__city_code=city_code, device_id__village_code=village_code)
        else:
            pass
    except Exception, e:
        print(str(e))
        pass
    total_page = int(math.ceil(len(device_list)/15.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_device/health/?page="+str(total_page))
    start_num = (page - 1) * 15
    end_num = page * 15
    device_list = device_list[start_num:end_num]
    device_list = serializer(device_list, foreign=True)
    for device in device_list:
        try:
            device["tempBT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["tempBT"])))
        except Exception, e:
            print(str(e))
            device["tempBT"] = ""
        try:
            print device["tempB"]
            print type(device["tempB"])
            if device["tempB"] == 1:
                device["tempB"] = u"报警"
            elif device["tempB"] == 0:
                device["tempB"] = u"取消报警"
        except:
            device["tempB"] = u"正常"
        try:
            city = City.objects.get(city_code=int(device["device_id"]["city_code"]))
            city_name = city.city_name
            village_name = Village.objects.get(city=city, village_code=int(device["device_id"]["village_code"])).village_name
            address = city_name + village_name
        except Exception, e:
            print(str(e))
            address = u"未安装"
        device["address"] = address

    print device_list
    return render(request, 'app/admin_deviceHealth.html', {
        "page": page,
        "page_num": total_page,
        "user": user,
        "city_code": "c" + str(city_code),
        "village_code": "v" + str(village_code),
        "device_list": device_list,
        "city_list": city_list,
        "village_list": village_list,
    })


def admin_device_leakage(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_leakage.html', {
        "user": user,
    })


def list(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
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
    try:
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
    except:
        device_list = None
    # print device_list
    return render(request, "app/device_list.html", {
        "device_list": device_list,
        "page_num": page_num,
        "page" : page,
        "user": user,
    })


@csrf_exempt
def instock(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        device_type = request.POST.get("type", None)
        device_number = request.POST.get("number", None)
        if device_type is None or device_number is None:
            return HttpResponse("error")
        device_number = int(device_number)
        start_num = 0
        print type(device_type)
        print device_type
        device_type = int(device_type)
        if device_type == 1:
            d_num = Device.objects.filter(device_id__lt=200000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 100000000 - 1
            device_type = u"终端"
        elif device_type == 2:
            d_num = Device.objects.filter(device_id__gte=200000000, device_id__lt=300000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 200000000 - 1
            device_type = u"中继"
        else:
            d_num = Device.objects.filter(device_id__gte=300000000).order_by('-id')
            if len(d_num) > 0:
                start_num = d_num[0].device_id
            else:
                start_num = 300000000 - 1
            device_type = u"网关"
        start_num = int(start_num)
        # start_num += 1
        start_no = start_num + 1
        for i in range(device_number):
            start_num += 1
            device = Device()
            device.device_id = start_num
            device.device_status = u"未安装"
            now = time.localtime()
            device.manufacture_date = datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            device.save()
            parameter = Parameter()
            parameter.device = device
            parameter.temperature_t_length = 60
            parameter.temperature = 60
            parameter.power_get_point1 = "00:00"
            parameter.power_get_point2 = "12:00"
            parameter.version = 1
            parameter.save()
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
        user = Adminer.objects.get(name=request.session['username'])
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


@csrf_exempt
def admin_device_gateway_parameter(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        if page < 1:
            return HttpResponseRedirect("/admin_device/gateway/parameter/?page=1")
        try:
            city_code = int(request.GET.get("city_code"))
        except:
            city_code = 0
        try:
            village_code = int(request.GET.get("village_code"))
        except:
            village_code = 0
        city_list = City.objects.all()
        try:
            city = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
        except:
            village_list = None
        gateway_list = Parameter.objects.filter()
        if city_code == 0 and village_code == 0:
            pass
        elif village_code == 0:
            gateway_list = gateway_list.filter(device__city_code=city_code)
        else:
            try:
                gateway_list = gateway_list.filter(device__city_code=city_code, device__village_code=village_code)
            except:
                pass
        start_num = (page - 1) * 15
        end_num = page * 15
        total_page = int(math.ceil(len(gateway_list))/15.0)
        gateway_list = gateway_list[start_num:end_num]
        if total_page < 1:
            total_page = 1
            # return HttpResponseRedirect("/admin_device/gateway/parameter/?page=" + str(total_page))
        if page > total_page:
            return HttpResponseRedirect("/admin_device/gateway/parameter/?page="+str(total_page))
        gateway_list = serializer(gateway_list, datetime_format='string', foreign=True)
        for gateway in gateway_list:
            print gateway
            device = Device.objects.get(device_id=int(gateway["device"]["device_id"]))
            try:
                city_name = City.objects.get(city_code=device.city_code).city_name
            except:
                city_name = ""
            try:
                village_name = Village.objects.get(village_code=device.village_code).village_name
            except:
                village_name = ""
            if city_name == "" and village_name == "":
                gateway["address"] = u"未安装"
            else:
                gateway["address"] = city_name + "" + village_name
            parameter = Parameter.objects.get(id=int(gateway["id"]))
            gateway["power_get_point1"] = str(parameter.power_get_point1)
            gateway["power_get_point2"] = str(parameter.power_get_point2)

        return render(request, "app/admin_gateway_parameter.html",{
            "gateway_list": gateway_list,
            "city_list": city_list,
            "village_list": village_list,
            "page": page,
            "total_page": total_page,
            "user": user,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
        })
    else:
        try:
            id = int(request.POST.get("id"))
            temperature_t_length = int(request.POST.get("temperature_t_length"))
            temperature = float(request.POST.get("temperature"))
            power_get_point1 = request.POST.get("power_get_point1")
            power_get_point2 = request.POST.get("power_get_point2")
            print(id)
            print(temperature)
            print(temperature_t_length)
            print(power_get_point1)
            print(power_get_point2)
            parameter = Parameter.objects.get(id=id)
            parameter.temperature_t_length = temperature_t_length
            parameter.temperature = temperature
            parameter.power_get_point1 = power_get_point1
            parameter.power_get_point2 = power_get_point2
            parameter.version += 1
            parameter.save()
            return HttpResponse("success")
        except Exception, e:
            print(str(e))
            return HttpResponse("error")
        return HttpResponse("POST")


@csrf_exempt
def admin_device_info(request, device_id):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        try:
            device = Device.objects.get(device_id=device_id)
            device_serializer = serializer(device)
            try:
                city = City.objects.get(city_code=int(device_serializer["city_code"]))
                device_serializer["city_code"] = city.city_name
                village = Village.objects.get(village_code=int(device_serializer["village_code"]), city=city)
                device_serializer["village_code"] = village.village_name
            except:
                pass
            device_serializer["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(device_serializer["manufacture_date"]))
            return HttpResponse(json.dumps(device_serializer))
        except Exception, e:
            print str(e)
            return HttpResponse("error")
    else:
        return HttpResponse("error")



from datetime import timedelta
import calendar
# 管理中继采集到的数据
@csrf_exempt
def admin_relay_data(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        if page < 1:
            return HttpResponseRedirect("/admin_relay/data/?page=1")

        try:
            city_code = int(request.GET.get("city_code"))
        except:
            city_code = 0
        try:
            village_code = int(request.GET.get("village_code"))
        except:
            village_code = 0
        city_list = City.objects.all()
        try:
            city = City.objects.get(city_code=city_code)
            village_list = Village.objects.filter(city=city)
        except:
            village_list = None
        device_list = Device.objects.filter(device_id__gte=200000000, device_id__lt=300000000)
        if city_code == 0 and village_code == 0:
            pass
        elif village_code == 0:
            device_list = device_list.filter(city_code=city_code)
        else:
            try:
                device_list = device_list.filter(city_code=city_code, village_code=village_code)
            except:
                pass
        start_num = (page - 1) * 15
        end_num = page * 15
        total_page = int(math.ceil(len(device_list)) / 15.0)
        device_list = device_list[start_num:end_num]
        device_list = serializer(device_list)
        for device in device_list:
            try:
                city = City.objects.get(city_code=int(device["city_code"]))
                city_name = city.city_name
                village_name = Village.objects.get(city=city, village_code=int(device["village_code"])).village_name
                address = city_name + village_name
            except:
                address = u"未安装"
            device["address"] = address
            device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["manufacture_date"])))
        if total_page < 1:
            total_page = 1
        if page > total_page:
            return HttpResponseRedirect("/admin_relay/data/?page=" + str(total_page))
        try:
            device_id = int(request.GET.get('device_id'))
            device = Device.objects.get(device_id=device_id)
            print device
            try:
                start_time = request.GET.get("relay_data_start_time")
                end_time = request.GET.get("relay_data_end_time")
                start_time = datetime.strptime(start_time, "%Y-%m-%d")
                end_time = datetime.strptime(end_time, "%Y-%m-%d")
            except Exception as e:
                print(str(e))
                today = datetime.today()
                start_time = datetime(today.year, today.month, today.day)
                end_time = datetime(today.year, today.month, today.day) + timedelta(days=1)
            relay_list = Relay.objects.filter(device_id=device, data_time__gte=start_time, data_time__lte=end_time).order_by('-data_time')
            latest = relay_list
            latest = serializer(latest)
            latest.reverse()
            for r in latest:
                r["data_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r["data_time"])))
            # 最近一月日用电量统计/用电总量及高峰低谷统计
            today = datetime.today()
            year = today.year
            month = today.month
            day = today.day
            init_day = datetime(year, month, 1)
            pre_day = init_day - timedelta(days=1)
            month_data = []
            power_sum = 0
            try:
                data = relay_list.filter(data_time__year=pre_day.year, data_time__month=pre_day.month,
                                         data_time__day=pre_day.day)[0]
                data_1 = relay_list.filter(data_time__year=year, data_time__month=month, data_time__day=day)[0]
                data_dic = {}
                data_dic["a_powerV"] = round(data_1.a_powerV - data.a_powerV, 2)
                data_dic["b_powerV"] = round(data_1.b_powerV - data.b_powerV, 2)
                data_dic["c_powerV"] = round(data_1.c_powerV - data.c_powerV, 2)
                data_dic["t_powerV"] = round(data_1.t_powerV - data.t_powerV, 2)
                data_dic["day"] = 1
                max_powerV = data_dic["t_powerV"]
                min_powerV = data_dic["t_powerV"]
                power_sum += data_dic["t_powerV"]
                month_data.append(data_dic)
            except Exception, e:
                print(str(e))
                data_dic = {}
                data_dic["a_powerV"] = 0
                data_dic["b_powerV"] = 0
                data_dic["c_powerV"] = 0
                data_dic["t_powerV"] = 0
                data_dic["day"] = 1
                max_powerV = data_dic["t_powerV"]
                min_powerV = data_dic["t_powerV"]
                power_sum += data_dic["t_powerV"]
                month_data.append(data_dic)
            # month_days_num = calendar.monthrange(year, month)[1]
            for i in range(2, day + 1):
                print "i=", i
                data_today = datetime(year, month, i)
                print data_today
                try:
                    yesterday_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                    print "yes", yesterday_data
                    data_today = data_today + timedelta(days=1)
                    today_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                    print "Tod", today_data
                    data_dic = {}
                    data_dic["a_powerV"] = round(today_data.a_powerV - yesterday_data.a_powerV, 2)
                    data_dic["b_powerV"] = round(today_data.b_powerV - yesterday_data.b_powerV, 2)
                    data_dic["c_powerV"] = round(today_data.c_powerV - yesterday_data.c_powerV, 2)
                    data_dic["t_powerV"] = round(today_data.t_powerV - yesterday_data.t_powerV, 2)
                    data_dic["day"] = i
                    if data_dic["t_powerV"] < min_powerV:
                        min_powerV = data_dic["t_powerV"]
                    if data_dic["t_powerV"] > max_powerV:
                        max_powerV = data_dic["t_powerV"]
                    power_sum += data_dic["t_powerV"]
                    month_data.append(data_dic)
                except Exception, e:
                    print str(1), str(i), str(e)
                    try:
                        data_today = data_today + timedelta(days=1)
                        print data_today
                        today_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                        data_dic = {}
                        data_dic["a_powerV"] = today_data.a_powerV
                        data_dic["b_powerV"] = today_data.b_powerV
                        data_dic["c_powerV"] = today_data.c_powerV
                        data_dic["t_powerV"] = today_data.t_powerV
                        data_dic["day"] = i
                        if data_dic["t_powerV"] < min_powerV:
                            min_powerV = data_dic["t_powerV"]
                        if data_dic["t_powerV"] > max_powerV:
                            max_powerV = data_dic["t_powerV"]
                        power_sum += data_dic["t_powerV"]
                        month_data.append(data_dic)
                    except Exception, e:
                        print str(2), str(i), str(e)
                        data_dic = {}
                        data_dic["a_powerV"] = 0
                        data_dic["b_powerV"] = 0
                        data_dic["c_powerV"] = 0
                        data_dic["t_powerV"] = 0
                        data_dic["day"] = i
                        if data_dic["t_powerV"] < min_powerV:
                            min_powerV = data_dic["t_powerV"]
                        if data_dic["t_powerV"] > max_powerV:
                            max_powerV = data_dic["t_powerV"]
                        power_sum += data_dic["t_powerV"]
                        month_data.append(data_dic)
            ret_data = {}
            ret_data["latest"] = latest
            ret_data["device_id"] = device_id
            ret_data["month_data"] = month_data
            ret_data["max_powerV"] = max_powerV
            ret_data["min_powerV"] = min_powerV
            ret_data["power_sum"] = power_sum
            ret_data["start_time"] = str(start_time)[0:10]
            ret_data["end_time"] = str(end_time)[0:10]
            ret_data = json.dumps(ret_data)
            print ret_data
        except Exception as e:
            print(str(e))
            ret_data = {}
            pass
        return render(request, "app/admin_relay_data.html", {
            'ret_data': ret_data,
            'page': page,
            'total_page': total_page,
            'device_list': device_list,
            'city_list': city_list,
            'village_list': village_list,
            'city_code': city_code,
            "city_code": "c" + str(city_code),
            "village_code": "v" + str(village_code),
        })
    else:
        try:
            device_id = int(request.POST.get('device_id'))
        except:
            return HttpResponse("error")
        device = Device.objects.get(device_id=device_id)
        print device
        today = datetime.today()
        today = datetime(today.year, today.month, today.day, 0, 0, 0)
        relay_list = Relay.objects.filter(device_id=device, data_time__gt=today).order_by('-data_time')
        latest = relay_list
        latest = serializer(latest)
        latest.reverse()
        for r in latest:
            r["data_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r["data_time"])))
        # 最近一月日用电量统计/用电总量及高峰低谷统计
        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day
        init_day = datetime(year, month, 1)
        pre_day = init_day - timedelta(days=1)
        month_data = []
        power_sum = 0
        try:
            data = relay_list.filter(data_time__year=pre_day.year, data_time__month=pre_day.month, data_time__day=pre_day.day)[0]
            data_1 = relay_list.filter(data_time__year=year, data_time__month=month, data_time__day=day)[0]
            data_dic = {}
            data_dic["a_powerV"] = round(data_1.a_powerV - data.a_powerV,2)
            data_dic["b_powerV"] = round(data_1.b_powerV - data.b_powerV,2)
            data_dic["c_powerV"] = round(data_1.c_powerV - data.c_powerV,2)
            data_dic["t_powerV"] = round(data_1.t_powerV - data.t_powerV,2)
            data_dic["day"] = 1
            max_powerV = data_dic["t_powerV"]
            min_powerV = data_dic["t_powerV"]
            power_sum += data_dic["t_powerV"]
            month_data.append(data_dic)
        except Exception, e:
            print(str(e))
            data_dic = {}
            data_dic["a_powerV"] = 0
            data_dic["b_powerV"] = 0
            data_dic["c_powerV"] = 0
            data_dic["t_powerV"] = 0
            data_dic["day"] = 1
            max_powerV = data_dic["t_powerV"]
            min_powerV = data_dic["t_powerV"]
            power_sum += data_dic["t_powerV"]
            month_data.append(data_dic)
        # month_days_num = calendar.monthrange(year, month)[1]
        for i in range(2, day + 1):
            print "i=", i
            data_today = datetime(year, month, i)
            print data_today
            try:
                yesterday_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                print "yes", yesterday_data
                data_today = data_today + timedelta(days=1)
                today_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                print "Tod", today_data
                data_dic = {}
                data_dic["a_powerV"] = round(today_data.a_powerV - yesterday_data.a_powerV,2)
                data_dic["b_powerV"] = round(today_data.b_powerV - yesterday_data.b_powerV,2)
                data_dic["c_powerV"] = round(today_data.c_powerV - yesterday_data.c_powerV,2)
                data_dic["t_powerV"] = round(today_data.t_powerV - yesterday_data.t_powerV,2)
                data_dic["day"] = i
                if data_dic["t_powerV"] < min_powerV:
                    min_powerV = data_dic["t_powerV"]
                if data_dic["t_powerV"] > max_powerV:
                    max_powerV = data_dic["t_powerV"]
                power_sum += data_dic["t_powerV"]
                month_data.append(data_dic)
            except Exception,e:
                print str(1), str(i),str(e)
                try:
                    data_today = data_today + timedelta(days=1)
                    print data_today
                    today_data = relay_list.filter(data_time__lt=data_today).order_by('-data_time')[0]
                    data_dic = {}
                    data_dic["a_powerV"] = today_data.a_powerV
                    data_dic["b_powerV"] = today_data.b_powerV
                    data_dic["c_powerV"] = today_data.c_powerV
                    data_dic["t_powerV"] = today_data.t_powerV
                    data_dic["day"] = i
                    if data_dic["t_powerV"] < min_powerV:
                        min_powerV = data_dic["t_powerV"]
                    if data_dic["t_powerV"] > max_powerV:
                        max_powerV = data_dic["t_powerV"]
                    power_sum += data_dic["t_powerV"]
                    month_data.append(data_dic)
                except Exception,e:
                    print str(2), str(i),str(e)
                    data_dic = {}
                    data_dic["a_powerV"] = 0
                    data_dic["b_powerV"] = 0
                    data_dic["c_powerV"] = 0
                    data_dic["t_powerV"] = 0
                    data_dic["day"] = i
                    if data_dic["t_powerV"] < min_powerV:
                        min_powerV = data_dic["t_powerV"]
                    if data_dic["t_powerV"] > max_powerV:
                        max_powerV = data_dic["t_powerV"]
                    power_sum += data_dic["t_powerV"]
                    month_data.append(data_dic)
        ret_data = {}
        ret_data["latest"] = latest
        ret_data["month_data"] = month_data
        ret_data["max_powerV"] = max_powerV
        ret_data["min_powerV"] = min_powerV
        ret_data["power_sum"] = power_sum
        try:
            return HttpResponse(json.dumps(ret_data))
        except Exception, e:
            print(str(e))
            return HttpResponse("error")