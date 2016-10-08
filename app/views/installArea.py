# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, City, Village
from django.contrib.auth.hashers import check_password


def area_list(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        city_code = int(request.POST.get("city_code"))
    except:
        city_code = 0
    try:
        village_code = int(request.POST.get("village_code"))
    except:
        village_code = 0

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
    })