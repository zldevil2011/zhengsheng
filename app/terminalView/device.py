# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, Data
from django.contrib.auth.hashers import check_password
from datetime import datetime, date, timedelta
@csrf_exempt
def terminal_device_info(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    device = user.device
    try:
        data = Data.objects.filter(device_id=device).order_by('-powerT')[0]
    except:
        data = None
    # 获取当前设备的今日温度曲线
    now = datetime.now()
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    datas = Data.objects.filter(tempT__year=year, tempT__month=month, tempT__day=day).order_by('tempT')

    temperature = []
    for d in datas:
        temperature.append(d.temp)
    print temperature

    return render(request, 'terminalUser/terminal_device_info.html', {
        'user': user,
        'device': device,
        'data': data,
        'temperature': temperature,
        'voltage': temperature,
        'electricity': temperature,
    })