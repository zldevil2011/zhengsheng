# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, Fund
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
import calendar

# 计算用电明细，即当月总用电量和当月每天的用电明细

@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    # 获取当前用户对应的设备的10分钟每次的采集记录
    device = Device.objects.get(appuser=user)
    datas = Data.objects.filter(device=device).order_by('-time')[0:20]
    today = datetime.today()
    last_point_datetime = datetime(today.year, today.month, today.day, 23, 50, 0)
    last_point_datetime -= timedelta(days=today.day)

    try:
        fund = Fund.objects.filter(status=u"成功")[0]
        end_power = Data.objects.get(time=last_point_datetime).total_power
        month_power = datas[0].total_power - end_power
        month_time = str(today.year) + "-" + str(today.month)

    except Exception, e:
        print str(e)
        fund = None
        month_power = None
        month_time = None
    return render(request, 'terminalUser/terminal_details.html', {
        'user': user,
        'datas': datas,
        'fund': fund,
        'month_power': month_power,
        'month_time': month_time,
    })