
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


@csrf_exempt
def admin_device(request):
    return render(request, 'app/admin_device.html', {})


def admin_device_add(request):
    if request.method == "GET":
        return render(request, 'app/admin_deviceAdd.html', {})
    else:
        return HttpResponse("POST")


def admin_device_remove(request):
    if request.method == "GET":
        return render(request, 'app/admin_deviceRemove.html', {})
    else:
        return HttpResponse("POST")


def admin_device_location(request):
    return render(request, 'app/admin_deviceLocation.html', {})


def admin_device_maintain(request):
    return render(request, 'app/admin_deviceMaintain.html', {})


def admin_device_temperature(request):
    return render(request, 'app/admin_temperature.html', {})


def admin_device_health(request):
    return render(request, 'app/admin_deviceHealth.html', {})


def admin_device_leakage(request):
    return render(request, 'app/admin_leakage.html', {})