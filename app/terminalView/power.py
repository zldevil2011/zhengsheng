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

    datas = Data.objects.filter(device=device).order_by('-time')
    print datas.count()
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
    end_time = datetime(year, month, tmp_time_end.day, 23, 50)
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
    print "Day Data"
    print today_power
    today_data = {}
    today_data["today_power"] = today_power
    today_data["today_hour"] = today_hour
    # 计算当月数据,当月数据每次获取每天的power即为当天的总用电量
    # day += 1
    latest_data = datas[0]

    month_power = []
    month_day = []
    # month_day.append(str(latest_data.time.day) + "号")
    month_day.append(str(day) + "号")
    month_power.append(latest_data.power)
    init_time = datetime(year, month, day, 23, 50, 0) - timedelta(days=1)
    end_time = datetime(year, month, 1, 23, 50, 0)
    day_delta = timedelta(days=1)
    print init_time
    print end_time
    print datas.count()
    for data in datas:
        if data.time == end_time:
            month_power.append(data.power)
            month_day.append(str(data.time.day) + "号")
            break
        if data.time == init_time:
            print data.time
            month_power.append(data.power)
            month_day.append(str(data.time.day) + "号")
            init_time = init_time - day_delta
    print "EveryDay Data"
    print month_power
    month_power.reverse()
    month_day.reverse()
    month_data = {}
    month_data["month_power"] = month_power
    month_data["month_day"] = month_day

    # 计算年内每月的用电量,每月用电量用当月最后一天23:50的总电流-上一月最后一天23:50的总电流，total_power一年一清楚
    month_days = calendar.monthrange(year, month - 1)[1]
    print month_days
    latest_data = datas[0]
    year_power = []
    year_month = []
    year_month.append(str(month) + '月')
    year_power.append(latest_data.total_power)
    try:
        init_time = datetime(year, month - 1, month_days, 23, 50, 0)
        end_time = datetime(year - 1, 12, 31, 23, 50, 0)
        end_month_power = Data.objects.get(time=init_time).total_power
        month_delta = timedelta(days=month_days)
        init_time -= month_delta
        for data in datas:
            if data.time == end_time:
                tmp_power = end_month_power - data.total_power
                year_power.append(tmp_power)
                year_month.append(str(1) + "月")
                break
            if data.time == init_time:
                tmp_power = end_month_power - data.total_power
                end_month_power = data.total_power
                year_power.append(tmp_power)
                year_month.append(str(data.time.month + 1) + "月")
                month_days = calendar.monthrange(year, data.time.month)[1]
                init_time = init_time - timedelta(days=month_days)
        print year_month
        print year_power
        year_power.reverse()
        year_month.reverse()
    except:
        pass
    year_data = {}
    year_data["year_power"] = year_power
    year_data["year_month"] = year_month
    return render(request, 'terminalUser/terminal_electricity_info.html', {
        'user': user,
        'device': device,
        'data': data,
        'today_data': json.dumps(today_data, "application/json"),
        'month_data': json.dumps(month_data, "application/json"),
        'year_data': json.dumps(year_data, "application/json")
    })