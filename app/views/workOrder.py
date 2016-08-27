# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from app.models import AppUser, WorkOrder
from django.db.models import Q
import json

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


def work_order_filter(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except AppUser.DoesNotExist:
        return HttpResponseRedirect("/admin_login/")
    key = request.POST.get("key", None)
    page = request.POST.get("page", None)
    if key is None:
        key = ""
    work_order_list = WorkOrder.objects.filter(Q(content__icontains=key)|Q(type__icontains=key)|Q(classification__icontains=key))
    if page is None:
        page = 1
    page = int(page)
    start_line = (page - 1) * 20
    end_line = page * 20
    total_page = len(work_order_list)/20
    if len(work_order_list) - total_page * 20 > 0:
        total_page += 1
    work_order_list = work_order_list[start_line:end_line]
    work_order_list = serializers.serialize('json', work_order_list)
    ret_data = {}
    ret_data["page"] = page
    ret_data["total_page"] = total_page
    ret_data["data"] = work_order_list
    return HttpResponse(json.dumps(ret_data))

