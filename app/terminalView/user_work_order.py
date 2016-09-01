# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, WorkOrder
from django.contrib.auth.hashers import check_password
import time

@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/login/")
    wo_list = WorkOrder.objects.filter(user=user)
    return render(request, 'terminalUser/terminal_workOrder.html', {
        'user': user,
        'wo_list': wo_list,
    })


@csrf_exempt
def add_work_order(request):
    # return HttpResponse("success")
    try:
        user = AppUser.objects.get(username='zhengsheng')
        # user = AppUser.objects.get(username=request.session['username'])
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
        content=description,
        type=work_order_type,
        classification=work_order_classification,
        workOrderTime=time.strftime(ISOTIMEFORMAT, time.localtime()),
        status=u"待处理",
        user=user,
    )
    work_order.save()
    return HttpResponse("success")