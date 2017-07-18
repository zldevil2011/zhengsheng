# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, City, Village, Adminer, Device
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import json


def area_list(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        city_code = int(request.GET.get("city_code"))
    except:
        city_code = 0
    try:
        village_code = int(request.GET.get("village_code"))
    except:
        village_code = 0
    print city_code
    print village_code
    if city_code == 0 and village_code == 0:
        try:
            if user.level == 0:
                city = City.objects.filter()[0]
            else:
                city = City.objects.filter(adminer=user)[0]
            village_list = Village.objects.filter(city=city)
            if user.level == 0:
                city_list = City.objects.filter()
            else:
                city_list = City.objects.filter(adminer=user)
            city_code = city.city_code
        except:
            city_list = None
            village_list = None
            city_code = None
    else:
        try:
            city = City.objects.get(city_code = city_code)
            village_list = Village.objects.filter(city=city)
            if user.level == 0:
                city_list = City.objects.filter()
            else:
                city_list = City.objects.filter(adminer=user)
            city_code = city.city_code
        except:
            city_list = None
            village_list = None
            city_code = None

    return render(request, 'app/admin_area.html', {
        "city_list": city_list,
        "village_list": village_list,
        "city_code": city_code,
        "user": user,
    })


@csrf_exempt
def city_add(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponse("error")
    try:
        city_code = int(request.POST.get("city_code"))
    except Exception, e:
        print(str(e))
        return HttpResponse("error")
    try:
        city = City.objects.get(city_code=city_code)
        return HttpResponse("error")
    except:
        city_name = request.POST.get("city_name", None)
        if city_name is None:
            return HttpResponse("error")
        try:
            city = City()
            city.adminer = user
            city.city_code = city_code
            city.city_name = city_name
            city.save()
            return HttpResponse("success")
        except Exception, e:
            print(str(e))
            return HttpResponse("error")\


@csrf_exempt
def city_delete(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponse("error")
    try:
        city_code = int(request.POST.get("city_code"))
    except Exception, e:
        print(str(e))
        return HttpResponse("error")
    print "ok222"
    print city_code
    try:
        device_list = Device.objects.filter(city_code=city_code)
        print device_list
        for device in device_list:
            device.village_code = None
            device.city_code = None
            device.building_code = None
            device.unit_code = None
            device.room_code = None
            device.gateway_code = None
            device.meter_box = None
            device.device_status = u"未安装"
            device.save()
            try:
                appuser = AppUser.objects.get(device=device).delete()
            except Exception, e:
                print(str(e))
                pass
        city = City.objects.get(city_code=city_code)
        village_list = Village.objects.filter(city=city)
        for village in village_list:
            village.delete()
        city.delete()
        return HttpResponse("success")
    except Exception, e:
        print(str(e))
        print "faile"
        return HttpResponse("error")


@csrf_exempt
def village_add(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except Exception, e:
        print(str(e))
        return HttpResponse("error")
    print "111"
    try:
        city_code = int(request.POST.get("city_code"))
        village_code = int(request.POST.get("village_code"))
    except Exception, e:
        print(str(e))
        return HttpResponse("error")

    print "2222"
    try:
        city = City.objects.get(city_code=city_code)
        village_name = request.POST.get("village_name", None)
        print(village_name)
        print(village_code)
        if village_name is None:
            return HttpResponse("error")
        try:
            village = Village()
            village.village_code = village_code
            village.village_name = village_name
            village.city = city
            village.save()
            return HttpResponse("success")
        except Exception, e:
            print(str(e))
            return HttpResponse("error")
    except Exception, e:
        print(str(e))
        return HttpResponse("error")


@csrf_exempt
def village_delete(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponse("error")
    try:
        city_code = int(request.POST.get("city_code"))
        village_code = int(request.POST.get("village_code"))
    except Exception, e:
        print(str(e))
        return HttpResponse("error")
    try:
        device_list = Device.objects.filter(city_code=city_code, village_code=village_code)
        for device in device_list:
            device.village_code = None
            device.city_code = None
            device.building_code = None
            device.unit_code = None
            device.unit_code = None
            device.gateway_code = None
            device.meter_box = None
            device.device_status = u"未安装"
            device.save()
            try:
                appuser = AppUser.objects.get(device=device).delete()
            except:
                pass
    except:
        return HttpResponse("error")


@csrf_exempt
def city_village_list(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except Exception, e:
        return HttpResponse("error")
    try:
        city_code = int(request.POST.get("city_code"))
    except:
        return HttpResponse("error")
    try:
        village_list = Village.objects.filter(city__city_code=city_code)
        return HttpResponse(json.dumps(serializer(village_list)))
    except:
        return HttpResponse("error")

