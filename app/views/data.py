
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, City, Village
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import time
import math
from datetime import datetime, date, timedelta
import sys

@csrf_exempt
def admin_data(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    page = int(request.GET.get("page", 1))
    if page < 1:
        return HttpResponseRedirect("/admin_data?page=1")
    start_num = (page - 1) * 10
    end_num = (page) * 10
    city_code = 1001
    village_code = 1001
    city = City.objects.get(city_code=city_code)
    village = Village.objects.get(village_code=village_code)
    # 首先查找出属于该地区的所有终端
    device_list = Device.objects.filter(city_code=city_code, village_code=village_code)
    total_page = int(math.ceil(device_list.count()/10.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_data?page=" + str(total_page))
    village_device_list = device_list
    # 下面主要是对查看当前小区的翻页实现机器列表展示
    device_list = device_list[start_num:end_num]
    device_list = serializer(device_list)
    for device in device_list:
        address = city.city_name + village.village_name
        device["address"] = address
        if str(device["device_id"])[0:1] == "1":
            device["type"] = u"终端"
        elif str(device["device_id"])[0:1] == "2":
            device["type"] = u"中继"
        else:
            device["type"] = u"网关"
        device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["manufacture_date"])))
    # 日均最高最低用电量
    try:
        power_min = sys.maxint
    except:
        power_min = sys.maxsize
    power_max = -1
    day_min = 1
    day_max = 1
    # 总用电量
    power_total = 0
    # 终端数量
    device_num = 0
    # 正常数量
    device_success = 0
    # 异常数量
    device_error = 0
    for device in village_device_list:
        device_num += 1
        if device.device_status == u"正常":
            device_success += 1
        else:
            device_error += 1
    # 首先需要计算该小区当月的用电总量，按当月每天使用量统计的话，需要将该小区的所有终端的用电量求和（每天求和，做差）
    # 可以从1号开始算，每天的总和前去前一天的总和
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    yesterday = datetime(year, month, 1) - timedelta(days=1)
    yesterday_power = 0
    print("计算上一月最后一天的用电总量")
    for device in village_device_list:
        try:
            data = Data.objects.filter(device_id=device, powerT__year=yesterday.year, powerT__month=yesterday.month, powerT__day=yesterday.day).order_by('-powerT')[0]
            yesterday_power += data.powerV
        except Exception, e:
            print str(e)
            yesterday_power += 0
    print("开始计算每天的用电总量")
    month_power = []
    month_day = []
    for i in range(1, day + 1):
        today_power = 0
        for device in village_device_list:
            try:
                data = Data.objects.filter(device_id=device, powerT__year=today.year, powerT__month=today.month,
                                           powerT__day=i).order_by('-powerT')[0]
                today_power += data.powerV
            except Exception, e:
                print str(e)
                today_power += 0
        power_total += (today_power - yesterday_power)
        if today_power - yesterday_power > power_max:
            power_max = today_power - yesterday_power
            day_max = i
        if today_power - yesterday_power < power_min:
            power_min = today_power - yesterday_power
            day_min = i
        month_day.append(i)
        month_power.append(today_power - yesterday_power)
        yesterday_power = today_power
    day_max = str(day_max) + "日"
    day_min = str(day_min) + "日"
    print "当前小区当月每天的用电总量"
    print(month_day)
    print(month_power)
    month_data = {}
    month_data["month_day"] = month_day
    month_data["month_power"] = month_power

    # 计算当前小区过去一年的用电量统计，按月统计，即最后会有1-12个月数据，每个月的用电量等于当月最后一天的第二次电量采集量减去上一个最后一天的电量
    last_year_last_day = datetime(year, 1, 1) - timedelta(days=1)
    last_year_last_day_power = 0
    print("计算上一年最后一月最后一天的用电量")
    for device in village_device_list:
        try:
            data = Data.objects.filter(device_id=device, powerT__year=last_year_last_day.year, powerT__month=last_year_last_day.month, powerT__day=last_year_last_day.day).order_by('-powerT')[0]
            last_year_last_day_power += data.powerV
        except Exception, e:
            print str(e)
            last_year_last_day_power += 0
    print("开始计算每月的用电总量")
    year_power = []
    year_month = []
    for i in range(1, month + 1):
        month_power = 0
        for device in village_device_list:
            try:
                data = Data.objects.filter(device_id=device, powerT__year=today.year, powerT__month=i).order_by('-powerT')[0]
                month_power += data.powerV
            except Exception, e:
                print str(e)
                month_power += 0
        year_month.append(str(i))
        year_power.append(month_power - last_year_last_day_power)
        last_year_last_day_power = month_power
    print "当前小区当年每月的用电总量"
    print(year_month)
    print(year_power)
    year_data = {}
    year_data["year_month"] = year_month
    year_data["year_power"] = year_power


    # 计算今年和去年的对应月份的总用电量的比较吗，上面已经计算了今年的数据，所以直接计算去年的数据
    compare_max = -1
    for power in year_power:
        if power > compare_max:
            compare_max = power
    pre_year_last_day = datetime(year - 1, 1, 1) - timedelta(days=1)
    pre_year_last_day_power = 0
    print("计算前年最后一月最后一天的用电量")
    for device in village_device_list:
        try:
            data = Data.objects.filter(device_id=device, powerT__year=pre_year_last_day.year, powerT__month=pre_year_last_day.month).order_by('-powerT')[0]
            pre_year_last_day_power += data.powerV
        except Exception, e:
            print str(e)
            pre_year_last_day_power += 0
    print("开始计算去年每月的用电总量")
    pre_year_power = []
    pre_year_month = []
    for i in range(1, month + 1):
        month_power = 0
        for device in village_device_list:
            try:
                data = Data.objects.filter(device_id=device, powerT__year=today.year - 1, powerT__month=i).order_by('-powerT')[0]
                month_power += data.powerV
            except Exception, e:
                print str(e)
                month_power += 0
        if month_power - pre_year_last_day_power > compare_max:
            compare_max = month_power - pre_year_last_day_power
        pre_year_month.append(str(i))
        pre_year_power.append(month_power - pre_year_last_day_power)
        pre_year_last_day_power = month_power
    print "当前小区去年每月的用电总量"
    print(pre_year_month)
    print(pre_year_power)
    pre_year_data = {}
    pre_year_data["pre_year_month"] = pre_year_month
    pre_year_data["pre_year_power"] = pre_year_power
    return render(request, 'app/admin_data.html', {
        "device_list": device_list,
        "page": page,
        "total_page": total_page,
        "month_data": month_data,
        "day_max": day_max,
        "power_max": power_max,
        "day_min": day_min,
        "power_min": power_min,
        "power_total": power_total,
        "device_num": device_num,
        "device_success": device_success,
        "device_error": device_error,
        "year_data": year_data,
        "pre_year_data": pre_year_data,
        "compare_max": compare_max,
    })


