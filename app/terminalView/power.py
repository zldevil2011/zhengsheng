# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Device, Data
from django.contrib.auth.hashers import check_password
from datetime import datetime
from datetime import timedelta
from datetime import date
import calendar
import json

@csrf_exempt
def electricity_info(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    device = Device.objects.get(appuser=user)
    data = Data.objects.filter(device=device)[0]

    datas = Data.objects.all().order_by('-time')
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    now = datetime.now()
    hour = now.hour
    # 计算当天每时刻的电量
    today_power = []
    today_hour = []
    tmp_time_init = now - timedelta(hours=1)
    tmp_time_end = now - timedelta(days=1)
    today_hour.append(tmp_time_init.hour)
    init_time = datetime(tmp_time_init.year, tmp_time_init.month, tmp_time_init.day, tmp_time_init.hour, 0)
    end_time = datetime(year, month, tmp_time_end.day, 0, 0)
    hour_delta = timedelta(hours=1)
    for data in datas:
        if data.time == end_time:
            break
        if data.time == init_time:
            today_power.append(data.power)
            today_hour.append(str(data.time.hour) + "时")
            init_time = init_time - hour_delta
    today_hour.reverse()
    today_power.reverse()
    print today_power
    today_data = {}
    today_data["today_power"] = today_power
    today_data["today_hour"] = today_hour
    # 计算当月数据
    day += 12
    latest_data = datas[0]
    # month_days = calendar.monthrange(year, day)[1]
    month_power = []
    month_day = []
    month_day.append(str(latest_data.time.day) + "号")
    month_power.append(latest_data.power)
    init_time = datetime(year, month, day, 23, 50, 0) - timedelta(days=1)
    end_time = datetime(year, month, 1, 23, 50, 0)
    print init_time
    print end_time
    day_delta = timedelta(days=1)
    for data in datas:
        if data.time == end_time:
            month_power.append(data.power)
            month_day.append(str(data.time.day) + "号")
            break
        if data.time == init_time:
            month_power.append(data.power)
            month_day.append(str(data.time.day) + "号")
            init_time = init_time - day_delta
    print month_power
    month_power.reverse()
    month_day.reverse()
    month_data = {}
    month_data["month_power"] = month_power
    month_data["month_day"] = month_day
    return render(request, 'terminalUser/terminal_electricity_info.html', {
        'user': user,
        'device': device,
        'data': data,
        'today_data': json.dumps(today_data, "application/json"),
        'month_data': json.dumps(month_data, "application/json")
    })