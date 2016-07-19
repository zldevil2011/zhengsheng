
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


@csrf_exempt
def admin_account(request):
    return render(request, 'app/admin_account.html', {})


def admin_work_order(request):
    return render(request, 'app/admin_workOrder.html', {})


def admin_app_user(request):
    return render(request, 'app/admin_appUser.html', {})