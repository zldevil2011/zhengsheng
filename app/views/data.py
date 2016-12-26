
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, City, Village, Adminer
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import time
import math
from datetime import datetime, date, timedelta
import sys
import json

@csrf_exempt
def admin_data(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        city_code = int(request.GET.get("city_code"))
    except:
        city_code = 0
    try:
        village_code = int(request.GET.get("village_code"))
    except:
        village_code = 0
    print("CV_code:")
    print(city_code)
    print(village_code)
    city_list = City.objects.all()
    try:
        city = City.objects.get(city_code=city_code)
        village_list = Village.objects.filter(city=city)
    except:
        village_list = None
    print("CV:")
    print(city_list)
    print(village_list)

    device_list = Device.objects.exclude(device_status=u"未安装")
    if city_code == 0 and village_code == 0:
        pass
    elif village_code == 0:
        device_list = device_list.filter(city_code=city_code)
    else:
        try:
            device_list = device_list.filter(city_code=city_code, village_code=village_code)
        except:
            pass
    page = int(request.GET.get("page", 0))
    if page < 1:
        return HttpResponseRedirect("/admin_data?page=1")
    start_num = (page - 1) * 10
    end_num = (page) * 10
    # try:
    #     city_code = int(request.GET.get("city_code"))
    # except:
    #     city_code = 1001
    # try:
    #     village_code = int(request.GET.get("village_code"))
    # except:
    #     village_code = 1001
    # city_list = City.objects.all()
    # try:
    #     village_list = Village.objects.filter(city=city_list[0])
    # except:
    #     village_list = None

    # city = City.objects.get(city_code=city_code)
    # village = Village.objects.get(village_code=village_code)
    # 首先查找出属于该地区的所有终端
    # device_list = Device.objects.filter(city_code=city_code, village_code=village_code)
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
        city_name = City.objects.get(city_code=int(device["city_code"])).city_name
        city_tmp = City.objects.get(city_code=int(device["city_code"]))
        village_name = Village.objects.get(city=city_tmp, village_code=int(device["village_code"])).village_name
        address = city_name + village_name
        device["address"] = address
        if str(device["device_id"])[0:1] == "1":
            device["type"] = u"终端"
        elif str(device["device_id"])[0:1] == "2":
            device["type"] = u"中继"
        else:
            device["type"] = u"网关"
        device["manufacture_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(device["manufacture_date"])))
        t_device = Device.objects.get(device_id = int(device["device_id"]))
        appuser = AppUser.objects.get(device=t_device)
        device["user"] = appuser.username
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
        month_day.append(i)
        print "today_power: ", today_power
        if today_power != 0:
            month_power.append(today_power - yesterday_power)
            power_total += (today_power - yesterday_power)
            if today_power - yesterday_power > power_max:
                power_max = today_power - yesterday_power
                day_max = i
            if today_power - yesterday_power < power_min:
                power_min = today_power - yesterday_power
                day_min = i
            yesterday_power = today_power
        else:
            power_total += 0
            month_power.append(0)
            if today_power > power_max:
                power_max = today_power
                day_max = i
            if today_power < power_min:
                power_min = today_power
                day_min = i
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

    # 尝试将单台设备的当天、当月、当年的数据加入URL地址显示
    # 对于每个用户，有两种数据，当月每天用电量和当年每月用电量
    try:
        device_id = int(request.GET.get("device_id", None))
        device = Device.objects.get(device_id=device_id)
        try:
            start_time = request.GET.get("user_start_time", None)
            end_time = request.GET.get("user_end_time", None)
            start_time = datetime.strptime(start_time, "%Y-%m-%d")
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
        except Exception as e:
            print(str(e))
            today = datetime.today()
            start_time = datetime(today.year, today.month, today.day)
            end_time = datetime(today.year, today.month, today.day) + timedelta(days=1)
        print(device)
        print start_time
        print end_time
        today = date.today()
        year = today.year
        month = today.month
        day = today.day
        # 获取当前设备的今日采集数据
        day_data = {}
        day_x = []
        day_y = []
        datas_list_today = Data.objects.filter(device_id=device, date_time__gte=start_time,date_time__lte=end_time).order_by('-date_time')
        datas_list_today.reverse()
        try:
            for data in datas_list_today:
                day_x.append(str(data.date_time))
                day_y.append(data.powerV)
        except:
            datas_list_today = None
        day_data["day_x"] = day_x
        day_data["day_y"] = day_y
        # 获取电压有效值
        voltage_data = {}
        voltage_x = []
        voltage_y = []
        try:
            for data in datas_list_today:
                voltage_x.append(str(data.date_time))
                voltage_y.append(data.voltage)
        except:
            datas_list_today = None
        voltage_data["voltage_x"] = voltage_x
        voltage_data["voltage_y"] = voltage_y
        # 获取电流有效值
        electric_current_data = {}
        electric_current_x = []
        electric_current_y = []
        try:
            for data in datas_list_today:
                electric_current_x.append(str(data.date_time))
                electric_current_y.append(data.electric_current)
        except:
            datas_list_today = None
        electric_current_data["electric_current_x"] = electric_current_x
        electric_current_data["electric_current_y"] = electric_current_y
        # 获取功率因数
        power_factor_data = {}
        power_factor_x = []
        power_factor_y = []
        try:
            for data in datas_list_today:
                power_factor_x.append(str(data.date_time))
                power_factor_y.append(data.power_factor)
        except:
            datas_list_today = None
        power_factor_data["power_factor_x"] = power_factor_x
        power_factor_data["power_factor_y"] = power_factor_y
        # 获取有功功率
        active_power_data = {}
        active_power_x = []
        active_power_y = []
        try:
            for data in datas_list_today:
                active_power_x.append(str(data.date_time))
                active_power_y.append(data.active_power)
        except:
            datas_list_today = None
        active_power_data["active_power_x"] = active_power_x
        active_power_data["active_power_y"] = active_power_y
        # 获取无功功率
        reactive_power_data = {}
        reactive_power_x = []
        reactive_power_y = []
        try:
            for data in datas_list_today:
                reactive_power_x.append(str(data.date_time))
                reactive_power_y.append(data.reactive_power)
        except:
            datas_list_today = None
        reactive_power_data["reactive_power_x"] = reactive_power_x
        reactive_power_data["reactive_power_y"] = reactive_power_y

        # 计算当月每天的用电量，用当天的采集量减去昨天的采集量即为当天的用电量
        # 首先，计算当月1号 则先获取上月最后一次的采集量
        # 统计当前设备当月的用电高峰日期，低谷日期，总用电量
        try:
            user_power_min = sys.maxint
        except:
            user_power_min = sys.maxsize
        user_power_max = -1
        user_day_min = 1
        user_day_max = 1
        user_power_total = 0

        yesterday = datetime(year, month, 1) - timedelta(days=1)
        yesterday_power = 0
        try:
            yesterday_power = Data.objects.filter(device_id=device, date_time__year=yesterday.year, date_time__month=yesterday.month).order_by('-date_time')[0].powerV
        except:
            yesterday_power = 0
        print "YYYY"
        try:
            datas_list = Data.objects.filter(device_id=device, date_time__year=year, date_time__month=month).order_by('-date_time')
            month_day = []
            month_power = []
        except Exception, e:
            datas_list = None
            month_day = []
            month_power = []
            print str(e)
        print "ZZZ"
        for i in range(1, day + 1):
            print(i)
            try:
                today_power = datas_list.filter(date_time__day=i).order_by('-date_time')[0].powerV
            except Exception, e:
                print(str(e))
                today_power = 0
            print("check")
            print("today_power:" + str(today_power))
            month_day.append(i)
            try:
                if today_power != 0:
                    user_power_total += (today_power - yesterday_power)
                    month_power.append(today_power - yesterday_power)
                    if today_power - yesterday_power > user_power_max:
                        user_power_max = today_power - yesterday_power
                        user_day_max = i
                    if today_power - yesterday_power < user_power_min:
                        user_power_min = today_power - yesterday_power
                        user_day_min = i
                    yesterday_power = today_power
                else:
                    user_power_total += 0
                    month_power.append(0)
                    if today_power > user_power_max:
                        user_power_max = today_power
                        user_day_max = i
                    if today_power < user_power_min:
                        user_power_min = today_power
                        user_day_min = i
            except Exception, e:
                print(str(e))
        print("get user today info")
        month_data = {}
        month_data["month_day"] = month_day
        month_data["month_power"] = month_power
        print "xxxxx"
        # 计算当前用户当年每月用电量数据
        # 从今年1月份开始，用当月最后一天的数据减去上一个月最后一天的数据即为当月所用电量
        pre_month_last_day = datetime(year, 1, 1) - timedelta(days=1)
        pre_month_last_power = 0
        try:
            pre_month_last_power = Data.objects.filter(device=device, date_time__year=pre_month_last_day.year,date_time__month=pre_month_last_day.month).order_by('-date_time')[0]
        except:
            pre_month_last_power = 0
        print "去年12月份最后一次采集量", pre_month_last_power
        try:
            datas_list = Data.objects.filter(device_id=device, date_time__year=year).order_by('-date_time')
            year_month = []
            year_power = []
        except Exception, e:
            datas_list = None
            year_month = []
            year_power = []
            print str(e)
        for i in range(1, month + 1):
            try:
                month_power = datas_list.filter(date_time__month=i).order_by('-date_time')[0].powerV
            except:
                month_power = 0
            year_month.append(i)
            if month_power != 0 and month_power is not None:
                year_power.append(month_power - pre_month_last_power)
                pre_month_last_power = month_power
            else:
                year_power.append(0)
        print "xppxpxpxp"
        device_id = device.device_id
        year_data = {}
        year_data["year_month"] = year_month
        year_data["year_power"] = year_power
        ret_data = {}
        ret_data["device_id"] = str(device_id)
        ret_data["day"] = day_data
        ret_data["voltage_data"] = voltage_data
        ret_data["electric_current_data"] = electric_current_data
        ret_data["power_factor_data"] = power_factor_data
        ret_data["active_power_data"] = active_power_data
        ret_data["reactive_power_data"] = reactive_power_data
        ret_data["month"] = month_data
        ret_data["year"] = year_data
        ret_data["user_power_total"] = user_power_total
        ret_data["user_power_max"] = user_power_max
        ret_data["user_day_max"] = str(user_day_max) + "号"
        ret_data["user_power_min"] = user_power_min
        ret_data["user_day_min"] = str(user_day_min) + "号"
    except:
        ret_data = {}
        pass

    return render(request, 'app/admin_data.html', {
        "ret_data": ret_data,
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
        # "village_list": village_list,
        # "city_list": city_list,
        "city_list": city_list,
        "village_list": village_list,
        "city_code": "c" + str(city_code),
        "village_code": "v" + str(village_code),
        "user":user,
    })


@csrf_exempt
def admin_user_data(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    # 对于每个用户，有两种数据，当月每天用电量和当年每月用电量
    device_id = request.POST.get("device_id", None)
    if device_id is None:
        return HttpResponse("error")
    device_id = int(device_id)
    try:
        device = Device.objects.get(device_id=device_id)
    except:
        return HttpResponse("error")
    print(device)
    today = date.today()
    year = today.year
    month = today.month
    day = today.day


    # 获取当前设备的今日采集数据
    day_data = {}
    day_x = []
    day_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-powerT')
        datas_list_today.reverse()
        for data in datas_list_today:
            day_x.append(str(data.powerT))
            day_y.append(data.powerV)
    except:
        datas_list_today = None
    day_data["day_x"] = day_x
    day_data["day_y"] = day_y
    # 获取电压有效值
    voltage_data = {}
    voltage_x = []
    voltage_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-date_time')
        datas_list_today.reverse()
        for data in datas_list_today:
            voltage_x.append(str(data.date_time))
            voltage_y.append(data.voltage)
    except:
        datas_list_today = None
    voltage_data["voltage_x"] = voltage_x
    voltage_data["voltage_y"] = voltage_y
    # 获取电流有效值
    electric_current_data = {}
    electric_current_x = []
    electric_current_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-date_time')
        datas_list_today.reverse()
        for data in datas_list_today:
            electric_current_x.append(str(data.date_time))
            electric_current_y.append(data.electric_current)
    except:
        datas_list_today = None
    electric_current_data["electric_current_x"] = electric_current_x
    electric_current_data["electric_current_y"] = electric_current_y
    # 获取功率因数
    power_factor_data = {}
    power_factor_x = []
    power_factor_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-date_time')
        datas_list_today.reverse()
        for data in datas_list_today:
            power_factor_x.append(str(data.date_time))
            power_factor_y.append(data.power_factor)
    except:
        datas_list_today = None
    power_factor_data["power_factor_x"] = power_factor_x
    power_factor_data["power_factor_y"] = power_factor_y
    # 获取有功功率
    active_power_data = {}
    active_power_x = []
    active_power_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-date_time')
        datas_list_today.reverse()
        for data in datas_list_today:
            active_power_x.append(str(data.date_time))
            active_power_y.append(data.active_power)
    except:
        datas_list_today = None
    active_power_data["active_power_x"] = active_power_x
    active_power_data["active_power_y"] = active_power_y
    # 获取无功功率
    reactive_power_data = {}
    reactive_power_x = []
    reactive_power_y = []
    try:
        datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month, powerT__day=day).order_by('-date_time')
        datas_list_today.reverse()
        for data in datas_list_today:
            reactive_power_x.append(str(data.date_time))
            reactive_power_y.append(data.reactive_power)
    except:
        datas_list_today = None
    reactive_power_data["reactive_power_x"] = reactive_power_x
    reactive_power_data["reactive_power_y"] = reactive_power_y



    # 计算当月每天的用电量，用当天的采集量减去昨天的采集量即为当天的用电量
    # 首先，计算当月1号 则先获取上月最后一次的采集量
    # 统计当前设备当月的用电高峰日期，低谷日期，总用电量
    try:
        user_power_min = sys.maxint
    except:
        user_power_min = sys.maxsize
    user_power_max = -1
    user_day_min = 1
    user_day_max = 1
    user_power_total = 0

    yesterday = datetime(year,  month, 1) - timedelta(days=1)
    yesterday_power = 0
    try:
        yesterday_power = Data.objects.filter(device_id=device, powerT__year=yesterday.year, powerT__month=yesterday.month).order_by('-powerT')[0].powerV
    except:
        yesterday_power = 0
    print "YYYY"
    try:
        datas_list = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month).order_by('-powerT')
        month_day = []
        month_power = []
    except Exception, e:
        datas_list = None
        month_day = []
        month_power = []
        print str(e)
    print "ZZZ"
    for i in range(1, day + 1):
        print(i)
        try:
            today_power = datas_list.filter(powerT__day=i).order_by('-powerT')[0].powerV
        except Exception,e:
            print(str(e))
            today_power = 0
        print("check")
        print("today_power:" + str(today_power))
        month_day.append(i)
        try:
            if today_power != 0:
                user_power_total += (today_power - yesterday_power)
                month_power.append(today_power - yesterday_power)
                if today_power - yesterday_power > user_power_max:
                    user_power_max = today_power - yesterday_power
                    user_day_max = i
                if today_power - yesterday_power < user_power_min:
                    user_power_min = today_power - yesterday_power
                    user_day_min = i
                yesterday_power = today_power
            else:
                user_power_total += 0
                month_power.append(0)
                if today_power > user_power_max:
                    user_power_max = today_power
                    user_day_max = i
                if today_power < user_power_min:
                    user_power_min = today_power
                    user_day_min = i
        except Exception, e:
            print(str(e))
    print("get user today info")
    month_data = {}
    month_data["month_day"] = month_day
    month_data["month_power"] = month_power
    print "xxxxx"
    # 计算当前用户当年每月用电量数据
    # 从今年1月份开始，用当月最后一天的数据减去上一个月最后一天的数据即为当月所用电量
    pre_month_last_day = datetime(year, 1, 1) - timedelta(days=1)
    pre_month_last_power = 0
    try:
        pre_month_last_power = Data.objects.filter(device=device, powerT__year=pre_month_last_day.year, powerT__month=pre_month_last_day.month).order_by('-powerT')[0]
    except:
        pre_month_last_power = 0
    print "去年12月份最后一次采集量", pre_month_last_power
    try:
        datas_list = Data.objects.filter(device_id=device, powerT__year=year).order_by('-powerT')
        year_month = []
        year_power = []
    except Exception, e:
        datas_list = None
        year_month = []
        year_power = []
        print str(e)
    for i in range(1, month + 1):
        try:
            month_power = datas_list.filter(powerT__month=i).order_by('-powerT')[0].powerV
        except:
            month_power = 0
        year_month.append(i)
        if month_power != 0 and month_power is not None:
            year_power.append(month_power - pre_month_last_power)
            pre_month_last_power = month_power
        else:
            year_power.append(0)
    print "xppxpxpxp"
    try:
        print "ok1"
        year_data = {}
        year_data["year_month"] = year_month
        year_data["year_power"] = year_power
        ret_data = {}
        # 最近的12条记录
        ret_data["day"] = day_data
        ret_data["voltage_data"] = voltage_data
        ret_data["electric_current_data"] = electric_current_data
        ret_data["power_factor_data"] = power_factor_data
        ret_data["active_power_data"] = active_power_data
        ret_data["reactive_power_data"] = reactive_power_data

        ret_data["month"] = month_data
        ret_data["year"] = year_data
        ret_data["user_power_total"] = user_power_total
        ret_data["user_power_max"] = user_power_max
        ret_data["user_day_max"] = str(user_day_max) + "号"
        ret_data["user_power_min"] = user_power_min
        ret_data["user_day_min"] = str(user_day_min) + "号"
        print "ok2"
        return HttpResponse(json.dumps(ret_data), "application/json")
    except Exception, e:
        print "not ok 1"
        ret_data = {}
        print str(e)
        return HttpResponse(json.dumps(ret_data), "application/json")