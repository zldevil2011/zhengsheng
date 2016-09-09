# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, Device, Fund
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
import calendar


@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/login/")
    device = Device.objects.get(appuser=user)
    datas = Data.objects.filter(device=device).order_by('-time')
    try:
        latest_data = datas[0]
        fund = Fund.objects.filter(appuser=user).order_by('-time')[0]
    except:
        latest_data = None
        fund = None
    fund_list = Fund.objects.filter(appuser=user, status=u"结算").order_by('-time')
    # print fund_list
    today = datetime.today()
    year = today.year
    month = today.month
    month_days = calendar.monthrange(year, month - 1)[1]
    init_time = datetime(year, month - 1, month_days, 23, 50, 0)
    end_time = datetime(year - 1, 12,  31, 23, 50, 0)
    init_power = Data.objects.get(time=init_time).total_power
    month_delta = timedelta(days=month_days)
    init_time -= month_delta
    power_list = []
    for data in datas:
        if init_time == end_time:
            tmp_power = init_power
            power_list.append(tmp_power)
            break
        if init_time == data.time:
            tmp = init_power - data.total_power
            init_power = data.total_power
            power_list.append(tmp)
            month_days = calendar.monthrange(year, data.time.month)[1]
            init_time = init_time - timedelta(days=month_days)

    ret_data = []
    fund_num = len(fund_list)
    for i in range(fund_num):
        data_dic = {}
        data_dic["fund"] = fund_list[i]
        data_dic["power"] = power_list[i]
        ret_data.append(data_dic)
    print ret_data
    return render(request, 'terminalUser/terminal_month_fees.html', {
        'latest_data': latest_data,
        'fund_list': fund_list,
        'power_list': power_list,
        'fund': fund,
        'ret_data': ret_data,
    })