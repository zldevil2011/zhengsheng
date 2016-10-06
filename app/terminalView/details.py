# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, Fund
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
import calendar
from dss.Serializer import serializer
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
    page = request.POST.get("page", None)
    if page is None:
        page = 1
    start_num = int(page - 1) * 20
    end_num = int(page) * 20
    device = user.device
    datas = Data.objects.filter(device_id=device).order_by('-powerT')
    today = datetime.today()
    last_point_datetime = datetime(today.year, today.month, today.day, 23, 50, 0)
    last_point_datetime -= timedelta(days=today.day)

    try:
        fund = Fund.objects.filter(status=u"成功")[0]
        end_power = Data.objects.get(time=last_point_datetime).total_power
        month_power = datas[0].total_power - end_power
        month_time = str(today.year) + "-" + str(today.month)
        total_page = int(math.ceil(datas.count()/20))
        datas = datas[start_num:end_num]

    except Exception, e:
        print str(e)
        fund = None
        month_power = None
        month_time = None
    if request.method == "GET":
        return render(request, 'terminalUser/terminal_details.html', {
            'user': user,
            'datas': datas,
            'fund': fund,
            'month_power': month_power,
            'month_time': month_time,
            'total_page': 1,
            'page': '1',
        })
    else:
        ret_data = {}
        ret_data["total_page"] = 1
        ret_data["data"] = serializer(datas)
        return HttpResponse(json.dumps(ret_data))