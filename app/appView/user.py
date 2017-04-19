# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data
from datetime import date, datetime
from django.contrib.auth.hashers import check_password,make_password
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def login(request):
    print "xxxx"
    if request.method == "GET":
        return render(request, "app_template/welcome.html", {})
    else:
        try:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            print username, password
            if username is None or password is None:
                return HttpResponse("error")
            try:
                user = User.objects.get(username=username)
                print user
                print password
                print user.password
                if check_password(password, user.password):
                    print "check ok"
                    appuser = AppUser.objects.get(user=user)

                    request.session['username'] = appuser.username
                    return HttpResponse("success")
                else:
                    print "not ok"
                    return HttpResponse("error")
            except Exception, e:
                print str(e)
                return HttpResponse("error")
        except Exception, e:
            print "Get Data"
            print(str(e))
            return HttpResponse("error")
@csrf_exempt
def logout(request):
    del request.session["username"]
    return HttpResponseRedirect("app/user/login/")


@csrf_exempt
def update(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    try:
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        address = request.POST.get("address", None)
        telephone = request.POST.get("telephone", None)
        if password != "":
            password = make_password(password, None, 'pbkdf2_sha256')
            user.user.password = password
            user.user.save()
        user.email = email
        user.address = address
        user.telephone = telephone
        user.save()
        return HttpResponse("success")
    except Exception, e:
        print str(e)
        return HttpResponse("error")


def index(request):
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
    today_start = datetime(year, month, day)
    # 获取今天已经采集的电能数据
    today_data = {}
    data = datas.filter(powerT__gte=today_start).order_by('-powerT')
    for d in data:
        if d.powerV is not None:
            today_data[d.powerT.hour] =  d.powerV
    print "Day Data"
    print today_data
    try:
        data = datas.order_by('-powerT')[0]
    except:
        data = None
    return render(request, 'app_template/index.html', {
        'user': user,
        'device': device,
        'data': data,
        'today_data': json.dumps(today_data, "application/json"),
    })
