# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Fund
from django.contrib.auth.hashers import check_password


@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    fund = Fund.objects.filter(appuser=user).order_by('-time')
    return render(request, 'terminalUser/terminal_fund.html', {
        'user': user,
        'fund': fund,
    })