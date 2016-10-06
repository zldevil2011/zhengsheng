# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password
from dss.Serializer import serializer
import json
import time
@csrf_exempt
def index(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    user = serializer(user)
    user["register_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user["register_time"]))
    print user
    print type(user)
    # user = json.dumps(user)
    # print user
    # print type(user)
    return render(request, 'terminalUser/terminal_index.html', {
        'user':user,
    })