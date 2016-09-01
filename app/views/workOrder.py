# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from app.models import AppUser, WorkOrder
from django.db.models import Q
import json
import time
import datetime
from dss.Serializer import serializer

def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    work_order_list = WorkOrder.objects.all()
    total_page = len(work_order_list) / 20
    if len(work_order_list) - total_page * 20 > 0:
        total_page += 1
    return render(request, 'app/admin_workOrder.html', {
        'work_order_list': work_order_list,
        'total_page': total_page,
        'page': 1,
    })


@csrf_exempt
def work_order_filter(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    try:
        key = request.POST.get("key", None)
        page = request.POST.get("page", None)
        startTime = request.POST.get("startTime", None)
        endTime = request.POST.get("endTime", None)
        if len(startTime) == 0:
            startTime = None
        if len(endTime) == 0:
            endTime = None
        if key is None:
            key = ""
        work_order_list = WorkOrder.objects.filter(Q(content__icontains=key)|Q(type__icontains=key)|Q(classification__icontains=key))
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
                    if order.workOrderTime < startTime:
                        tmp_flag = 0
                if endTime is not None:
                    print "endTTTTTTTTTTTTTTTTTT"
                    if order.workOrderTime > endTime:
                        tmp_flag = 0
                if tmp_flag == 1:
                    tmp.append(order)
            print tmp
        except Exception, e:
            print str(e)
        work_order_list = serializer(tmp)
        print work_order_list
        for i in range(len(work_order_list)):
            order = work_order_list[i]
            order["workOrderTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(order["workOrderTime"])))

        ret_data = {}
        ret_data["page"] = page
        ret_data["total_page"] = total_page
        ret_data["data"] = work_order_list
        return HttpResponse(json.dumps(ret_data), "application/json")
    except Exception, e:
        return HttpResponse("error")
