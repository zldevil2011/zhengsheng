# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, Data
from django.contrib.auth.hashers import check_password


@csrf_exempt
def electricity_info(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    device = Device.objects.get(appuser=user)
    data = Data.objects.filter(device=device)[0]

    return render(request, 'terminalUser/terminal_electricity_info.html', {
        'user': user,
        'device': device,
        'data': data,
    })