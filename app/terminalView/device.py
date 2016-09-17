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
    device = Device.objects.get(appuser=user)
    data = Data.objects.filter(device=device).order_by('-time')[0]
    # 获取当前设备的今日温度曲线
    now = datetime.now()
    today_now = datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    datas = Data.objects.filter(time__lte=today_now, time__gte=today_start).order_by('time')
    temperature = []
    for d in datas:
        temperature.append(d.temperature)
    print temperature


    time_delta_hour = timedelta(hours = 1)
    # 获取当前设备的电压曲线，按小时计
    start_time_hour0 = datetime(now.year, now.month, now.day, 0, 0, 0)
    voltage = []
    for d in datas:
        if d.time == start_time_hour0:
            voltage.append(d.voltage)
            start_time_hour0 += time_delta_hour

    # 获取当前设备的电流曲线，按小时计
    start_time_hour0 = datetime(now.year, now.month, now.day, 0, 0, 0)
    electricity = []
    for d in datas:
        if d.time == start_time_hour0:
            electricity.append(d.electricity)
            start_time_hour0 += time_delta_hour
    return render(request, 'terminalUser/terminal_device_info.html', {
        'user': user,
        'device': device,
        'data': data,
        'temperature': temperature,
        'voltage': voltage,
        'electricity': electricity,
    })