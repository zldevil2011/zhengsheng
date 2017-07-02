# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from app.models import AppUser, WorkOrder, Adminer
from django.db.models import Q
import json
import time
import datetime
from dss.Serializer import serializer
import math

def index(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    work_order_list = WorkOrder.objects.filter(adminer=user).order_by('-time')
    page = int(request.GET.get("page", 1))
    if page < 1:
        return HttpResponseRedirect("/admin_work_order?page=1")
    total_page = int(math.ceil(work_order_list.count() / 20.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_work_order?page=" + str(total_page))
    start_num = (page - 1) * 20
    end_num = page * 20
    work_order_list = work_order_list[start_num:end_num]
    work_order_list = serializer(work_order_list)
    for work in work_order_list:
        work["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(work["time"]))
    return render(request, 'app/admin_workOrder.html', {
        'work_order_list': work_order_list,
        'total_page': total_page,
        'page': page,
        "user":user,
    })


@csrf_exempt
def work_order_filter(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    try:
        key = request.POST.get("key", None)
        page = request.POST.get("page", None)
        startTime = request.POST.get("startTime", None)
        endTime = request.POST.get("endTime", None)
        print key
        print page
        print startTime
        print endTime
        if len(startTime) == 0:
            startTime = None
        if len(endTime) == 0:
            endTime = None
        if key is None:
            key = ""
        work_order_list = WorkOrder.objects.filter(Q(content__icontains=key)|Q(type__icontains=key)|Q(type__icontains=key)).order_by('-time')
        if page is None:
            page = 1
        page = int(page)
        start_line = (page - 1) * 20
        end_line = page * 20
        work_order_list = work_order_list[start_line:end_line]
        total_page = len(work_order_list)/20
        if len(work_order_list) - total_page * 20 > 0:
            total_page += 1
        try:
            today = datetime.date.today()
            if startTime is not None:
                print "startTime"
                startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d').date()
                startTime = datetime.datetime.now() - (today - startTime)
                print startTime
            if endTime is not None:
                endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d').date()
                endTime = datetime.datetime.now() - (today - endTime)
            tmp = []
            print "start save tmp"
            print startTime
            print endTime
            print type(startTime)
            print type(endTime)
            for order in work_order_list:
                tmp_flag = 1
                if startTime is not None:
                    print "startTTTTTTTTTTTTTTTTTTTT"
                    if order.time < startTime:
                        tmp_flag = 0
                if endTime is not None:
                    print "endTTTTTTTTTTTTTTTTTT"
                    if order.time > endTime:
                        tmp_flag = 0
                if tmp_flag == 1:
                    order.content = order.content.replace('<br>', '')[0:20] + "..."
                    tmp.append(order)
            print tmp
        except Exception, e:
            print str(e)
        work_order_list = serializer(tmp, foreign=True)
        print work_order_list
        for i in range(len(work_order_list)):
            order = work_order_list[i]
            order["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(order["time"])))

        ret_data = {}
        ret_data["page"] = page
        ret_data["total_page"] = total_page
        ret_data["data"] = work_order_list
        return HttpResponse(json.dumps(ret_data), "application/json")
    except Exception, e:
        return HttpResponse("error")


@csrf_exempt
def info(request, wo_id):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    if request.method == "GET":
        try:
            WO = WorkOrder.objects.get(pk=wo_id)
            return HttpResponse(json.dumps(serializer(WO, foreign=True)))
        except:
            return HttpResponse("error")
    else:
        try:
            ret_content = request.POST.get("ret_content", None)
            print ret_content
            if ret_content is None:
                return HttpResponse("error")
            wo = WorkOrder.objects.get(pk=wo_id)
            wo.content = wo.content + "<br>" + u"系统回复：" + unicode(ret_content)
            wo.status = u"正在处理"
            wo.save()
            return HttpResponse("success")
        except Exception, e:
            print str(e)
            return HttpResponse("error")

