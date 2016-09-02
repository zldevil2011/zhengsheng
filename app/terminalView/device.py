# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, Data
from django.contrib.auth.hashers import check_password


@csrf_exempt
def terminal_device_info(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    device = Device.objects.get(appuser=user)
    data = Data.objects.get(device=device)
    return render(request, 'terminalUser/terminal_device_info.html', {
        'user': user,
        'device': device,
        'data': data,
    })