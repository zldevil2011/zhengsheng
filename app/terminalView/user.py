# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password


@csrf_exempt
def login(request):
    print "xxxx"
    if request.method == "GET":
        return render(request, "terminalUser/terminal_login.html", {})
    else:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        # print username, password
        if username is None or password is None:
            return HttpResponse("error")
        try:
            user = AppUser.objects.get(username=username, password=password)
            request.session["username"] = user.username
            return HttpResponse("success")
        except Exception, e:
            print str(e)
            return HttpResponse("error")