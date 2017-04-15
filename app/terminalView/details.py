# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, Fund
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta, date
import calendar
from dss.Serializer import serializer
import time
import json
import math
# 计算用电明细，即当月总用电量和当月每天的用电明细

@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    # 获取当前用户对应的设备的10分钟每次的采集记录
    page = request.GET.get("page", None)
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        return HttpResponseRedirect("/terminal/details?page=1")
    # start_num = int(page - 1) * 20
    # end_num = int(page) * 20
    device = user.device
    datas = Data.objects.filter(device_id=device).order_by('-powerT')
    total_page = int(math.ceil(datas.count() / 20.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/terminal/details?page=" + str(total_page))
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    try:
        fund = None # Fund.objects.filter(status=u"成功")[0]
        try:
            today_power = datas.filter(powerT__year=today.year, powerT__month=today.month, powerT__day=today.day).order_by('-powerT')[0].powerV
        except:
            today_power = 0
        try:
            yesterday_power = datas.filter(powerT__year=yesterday.year, powerT__month=yesterday.month, powerT__day=yesterday.day).order_by('-powerT')[0].powerV
        except:
            yesterday_power = 0
        month_power = today_power - yesterday_power
        month_time = str(today.year) + "年"  + str(today.month) + '月' + str(today.day) + '日'
    except Exception, e:
        print str(e)
        fund = None
        month_power = None
        month_time = None
    # datas = datas[start_num:end_num]
    # 计算当天24小时的电量使用情况
    data_list = []
    hours = int(datetime.today().hour)
    for i in range(1, hours):
        try:
            tmp_data = {}
            start_time = datetime(datetime.today().year, datetime.today().month, datetime.today().day, i-1)
            end_time = start_time + timedelta(hours=1)
            start_data = datas.filter(powerT__gte=start_time)[0]
            end_data = datas.filter(powerT__lte=end_time)[-1]
            tmp_data["use"] = end_data.powerV - start_data.powerV
            tmp_data["total"] = end_data.powerV
            tmp_data["temp"] = end_data.temp
            tmp_data["time"] = i + "时"
            tmp_data["status"] = end_data.device_id.device_status
            data_list.append(tmp_data)
        except Exception as e:
            print(str(e))
    datas = serializer(datas, foreign=True)
    for data in datas:
        if data["powerT"] == None:
            pass
        else:
            data["powerT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["powerT"]))
    print(data_list)
    return render(request, 'terminalUser/terminal_details.html', {
        'user': user,
        'datas': datas,
        'fund': fund,
        'month_power': month_power,
        'month_time': month_time,
        'total_page': total_page,
        'page': page,
        'data_list':data_list,
    })