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
    device = user.device
    try:
        data = Data.objects.filter(device_id=device)[0]
    except:
        data = None
    datas = Data.objects.filter(device_id=device)
    print datas.count()
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    now = datetime.now()
    hour = now.hour
    # 获取今天已经采集的电能数据
    today_power = []
    today_hour = []
    data = datas.filter(powerT__year=year, powerT__month=month, powerT__day=day).order_by('-powerT')
    for d in data:
        if d.powerV is not None:
            today_power.append(d.powerV)
            today_hour.append(str(d.powerT.hour) + '时')
    today_power.reverse()
    today_hour.reverse()
    print "Day Data"
    print today_power
    print today_hour
    today_data = {}
    today_data["today_power"] = today_power
    today_data["today_hour"] = today_hour
    # 计算当月数据,当月数据每次获取当天的第二次采集减去前天的第二次采集点即为当天的总用电量
    month_power = []
    month_day = []
    try:
        yesterday = datetime(year, month, 1) - timedelta(days=1)
        try:
            pre_total = data.filter(powerT__year=yesterday.year, powerT__month=yesterday.month, powerT__day=yesterday.day).order_by('-powerT')[0].powerV
        except:
            pre_total = 0
        for i in range(1, day+1):
            try:
                data = datas.filter(powerT__year=year, powerT__month=month, powerT__day=i).order_by('-powerT')[0]
                month_day.append(str(data.powerT.day) + '号')
                month_power.append(data.powerV - pre_total)
                pre_total = data.powerV
            except:
                month_day.append(str(i) + '号')
                month_power.append(0)
    except:
        pass
    print "EveryDay Data"
    print month_power
    print month_day
    month_data = {}
    month_data["month_power"] = month_power
    month_data["month_day"] = month_day

    # 计算年内每月的用电量,每月用电量用当月最后一天的采集数量-上一月最后一天的采集量
    year_power = []
    year_month = []
    try:
        pre_month = datetime(year, 1, 1) - timedelta(days=1)
        try:
            pre_total = data.filter(powerT__year=pre_month.year, powerT__month=pre_month.month, powerT__day=pre_month.day).order_by('-powerT')[0].powerV
        except:
            pre_total = 0
        for i in range(1, month - 1):
            try:
                month_days = calendar.monthrange(year, i)[1]
                data = datas.filter(powerT__year=year, powerT__month=i).order_by('-powerT')[0]
                year_month.append(data.powerT.month + '月')
                year_power.append(data.powerV - pre_total)
                pre_total = data.powerV
            except:
                year_month.append(str(i) + '月')
                year_power.append(0)
    except:
        pre_total = 0
        pass
    # 由于当月不一定是最后一天，所以单独计算最新的数字
    try:
        data = datas.filter(powerT__year=year, powerT__month=month).order_by('-powerT')[0].powerV
        power = data - pre_total
    except:
        power = 0
    year_month.append(month)
    year_power.append(power)
    print "year Data"
    print year_month
    print year_power
    year_data = {}
    year_data["year_power"] = year_power
    year_data["year_month"] = year_month
    try:
        data = datas.order_by('-powerT')[0]
    except:
        data = None
    return render(request, 'terminalUser/terminal_electricity_info.html', {
        'user': user,
        'device': device,
        'data': data,
        'today_data': json.dumps(today_data, "application/json"),
        'month_data': json.dumps(month_data, "application/json"),
        'year_data': json.dumps(year_data, "application/json")
    })