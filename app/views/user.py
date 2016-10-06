# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password
import math

@csrf_exempt
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print username, password
    try:
        user = User.objects.get(username = username)
        print user.password
        if check_password(password, user.password):
            appuser = AppUser.objects.get(user=user)
            print "check ok"
            request.session['username'] = appuser.username
            return HttpResponse("success")
        else:
            return HttpResponse("error")
    except AppUser.DoesNotExist:
        return HttpResponse("error")


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
    try:
        page = request.GET.get("page", 1)
    except:
        pass
    page = int(page)
    if page < 1:
        page = 1
        return HttpResponseRedirect("/admin_account?page=1")
    start_num = (page - 1) * 10
    end_num = page * 10
    userlist = AppUser.objects.all()
    total_page = int(math.ceil(userlist.count()/10.0))
    if page > total_page:
        return HttpResponseRedirect("/admin_account?page=" +str(total_page))
    return render(request, 'app/admin_account.html', {
        "userlist" : userlist,
        "page": page,
        "total_page": total_page
    })


def admin_work_order(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_workOrder.html', {})