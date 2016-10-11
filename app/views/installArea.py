# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, City, Village, Adminer
from django.contrib.auth.hashers import check_password


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
        city = City.objects.all()[0]
        village_list = Village.objects.filter(city=city)
        city_list = City.objects.all()
        city_code = city.city_code
    else:
        city = City.objects.get(city_code = city_code)
        village_list = Village.objects.filter(city=city)
        city_list = City.objects.all()
        city_code = city.city_code

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
            city.city_code = city_code
            city.city_name = city_name
            city.save()
            return HttpResponse("success")
        except Exception, e:
            print(str(e))
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
        village_code = int(request.POST.get("city_code"))
    except Exception, e:
        print(str(e))
        return HttpResponse("error")

    print "2222"
    try:
        city = City.objects.get(city_code=city_code)
        village_name = request.POST.get("village_name", None)
        print(village_name)
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

