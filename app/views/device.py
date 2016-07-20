
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password


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