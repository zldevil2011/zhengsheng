# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Data, WorkOrder
from datetime import date, datetime
from django.contrib.auth.hashers import check_password,make_password
import json
import sys
import time
from dss.Serializer import serializer
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def login(request):
    print "xxxx"
    if request.method == "GET":
        try:
            user = AppUser.objects.get(username=request.session['username'])
            return HttpResponseRedirect("/app/index/")
        except Exception as e:
            print(str(e))
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
    return HttpResponseRedirect("/app/user/login/")


@csrf_exempt
def update(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/app/user/login/")
    if request.method == "GET":
        # 获取个人信息
        ret_data = {}
        ret_data["username"] = user.username
        ret_data["email"] = user.email
        ret_data["phone"] = user.telephone
        ret_data["address"] = user.address
        return HttpResponse(json.dumps(ret_data))
    else:
        try:
            operation = int(request.POST.get("operation"))
            if operation == 0:
                # 更新个人信息
                email = request.POST.get("email", None)
                address = request.POST.get("address", None)
                telephone = request.POST.get("phone", None)
                user.email = email
                user.address = address
                user.telephone = telephone
                user.save()
                user.user.email = email
                user.user.save()
                return HttpResponse("success")
            elif operation == 1:
                # 更新密码
                password = request.POST.get("password", None)
                if password != "":
                    password = make_password(password, None, 'pbkdf2_sha256')
                    user.user.password = password
                    user.user.save()
                return HttpResponse("success")
            else:
                return HttpResponse("error")
        except Exception as e:
            print(str(e))
            return HttpResponse("error")


def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/app/user/login/")
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
            today_data[d.powerT.hour] = d.powerV
    print "Day Data"
    print today_data
    # 获取今日的温度数据
    today_temperature_data = {}
    data = datas.filter(tempT__gte=today_start).order_by('-tempT')
    for d in data:
        if d.powerV is not None:
            today_temperature_data[d.tempT.hour] = d.temp
    print "Day Temperature Data"
    print today_temperature_data
    try:
        data = datas.order_by('-powerT')[0]
    except:
        data = None


    # 获取用户的工单
    workorder_list = WorkOrder.objects.filter(appuser=user)

    workorder_list = serializer(workorder_list)
    for wo in workorder_list:
        wo["content"] = wo["content"].replace("<br>"," ")
        wo["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wo["time"]))

    print workorder_list

    device = user.device
    user = serializer(user)
    user["device_install_time"] = str(device.manufacture_date)[0:10]
    return render(request, 'app_template/index.html', {
        'user': user,
        'device': device,
        'data': data,
        'workorder_list':workorder_list,
        'today_data': json.dumps(today_data, "application/json"),
        'today_temperature_data': json.dumps(today_temperature_data, "application/json"),
    })


@csrf_exempt
def workorder_info(request, wo_id):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/app/user/login/")
    if request.method == "GET":
        try:
            WO = WorkOrder.objects.get(pk=wo_id)
            ret_data = {}
            ret_data["type"] = WO.type
            ret_data["username"] = WO.appuser.username
            ret_data["phone"] = WO.appuser.telephone
            ret_data["email"] = WO.appuser.email
            ret_data["address"] = WO.appuser.address
            ret_data["content"] = WO.content.replace("<br>", "\n")
            ret_data["status"] = WO.status
            if ret_data["status"] == u"已处理":
                ret_data["status_tag"] = 1
            else:
                ret_data["status_tag"] = 0
            return HttpResponse(json.dumps(ret_data))
        except Exception as e:
            print(str(e))
            return HttpResponse("error")
    else:
        try:
            operation = int(request.POST.get("operation"))
            if operation == 1:
                # 回复工单
                work_order = WorkOrder.objects.get(pk=wo_id)
                content = request.POST.get("content", None)
                if content is None:
                    return HttpResponse("error")
                work_order.content = work_order.content + "<br>" + user.username + u"：" + unicode(content)
                work_order.save()
                return HttpResponse("success")
            elif operation == -1:
                # 关闭工单
                work_order = WorkOrder.objects.get(pk=wo_id)
                work_order.status = u"已处理"
                work_order.save()
                return HttpResponse("success")
            else:
                return HttpResponse("error")
        except Exception as e:
            print(str(e))
            return HttpResponse("error")


@csrf_exempt
def workorder_add(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/app/user/login/")
    try:
        username = request.POST.get("username", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        address = request.POST.get("address", None)
        content = request.POST.get("content", None)
        type = request.POST.get("type", None)
        if username is None or phone is None or email is None or address is None or content is None:
            return HttpResponse("error")
        import uuid
        num = uuid.uuid1()
        ISOTIMEFORMAT = '%Y-%m-%d%X'
        work_order = WorkOrder(
            num=num,
            content=user.username + u"：" + content,
            type=type,
            time=time.strftime(ISOTIMEFORMAT, time.localtime()),
            status=u"待处理",
            appuser=user,
        )
        work_order.save()
        return HttpResponse("success")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")