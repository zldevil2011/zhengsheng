
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password


@csrf_exempt
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    try:
        user = AppUser.objects.get(username = username)
        request.session['username'] = username
    except AppUser.DoesNotExist:
        return HttpResponse("error")
    return HttpResponse("success")


@csrf_exempt
def logout(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    del request.session['username']
    return HttpResponseRedirect("/admin_login/")


@csrf_exempt
def admin_account(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_account.html', {})


def admin_work_order(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_workOrder.html', {})