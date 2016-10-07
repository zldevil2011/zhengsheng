# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, WorkOrder
from django.contrib.auth.hashers import check_password
import time
import json
from dss.Serializer import serializer
import math

@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/login/")
    page = request.GET.get("page", None)
    if page is None:
        page = 1
    else:
        page = int(page)
    if page < 1:
        return HttpResponseRedirect("/terminal/work_order?page=1")

    wo_list = WorkOrder.objects.filter(appuser=user).order_by('-time')
    total_page = int(math.ceil(wo_list.count()/10.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/terminal/work_order?page=" + str(total_page))
    start_num = (page - 1) * 10
    end_num = page * 10
    wo_list = wo_list[start_num:end_num]
    wo_list = serializer(wo_list)
    for wo in wo_list:
        wo['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wo["time"]))
    return render(request, 'terminalUser/terminal_workOrder.html', {
        'user': user,
        'wo_list': wo_list,
        'page': page,
        'total_page': total_page
    })


@csrf_exempt
def add_work_order(request):
    # return HttpResponse("success")
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except AppUser.DoseNotExsit:
        return HttpResponseRedirect("/terminal/login/")
    # username = request.POST.get("username", None)
    # phone = request.POST.get("phone", None)
    # user_email = request.POST.get("userEmail", None)
    # address = request.POST.get("address", None)
    work_order_type = request.POST.get("workOrderType", None)
    work_order_classification = request.POST.get("workOrderClassification", None)
    description = request.POST.get("description", None)
    if work_order_type is None or work_order_classification is None:
        return HttpResponse("error")
    max_id = WorkOrder.objects.all()
    max_id = max_id.order_by('-id')
    if len(max_id) == 0:
        max_id = 0
    else:
        max_id = max_id[0].id + 1

    num = "WO_" + str(max_id)
    ISOTIMEFORMAT ='%Y-%m-%d%X'
    work_order = WorkOrder(
        num=num,
        content=user.username + u"：" + description,
        type=work_order_type,
        time=time.strftime(ISOTIMEFORMAT, time.localtime()),
        status=u"待处理",
        appuser=user,
    )
    work_order.save()
    return HttpResponse("success")


@csrf_exempt
def info(request, wo_id):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except AppUser.DoseNotExsit:
        return HttpResponseRedirect("/terminal/login/")
    if request.method == "GET":
        try:
            WO = WorkOrder.objects.get(pk=wo_id)
            return HttpResponse(json.dumps(serializer(WO, foreign=True)))
        except:
            return HttpResponse("error")
    else:
        try:
            ret_content = request.POST.get("ret_content", None)
            if ret_content is not None:
                wo = WorkOrder.objects.get(pk=wo_id)
                wo.content = wo.content + "<br>" + user.username + u"：" + unicode(ret_content)
                wo.status = u"正在处理"
                wo.save()
                return HttpResponse("success")
            else:
                try:
                    closeWO = request.POST.get("closeWO", None)
                    print closeWO
                    if closeWO == "true":
                        wo = WorkOrder.objects.get(pk=wo_id)
                        wo.status = u"已处理"
                        wo.save()
                        return HttpResponse("success")
                    else:
                        return HttpResponse("error")
                except:
                    return HttpResponse("error")
        except Exception, e:
            print str(e)
            return HttpResponse("error")