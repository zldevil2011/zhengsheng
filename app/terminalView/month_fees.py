# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password


@csrf_exempt
def index(request):
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/login/")
    return render(request, 'terminalUser/terminal_month_fees.html', {})