# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser
from django.contrib.auth.hashers import check_password,make_password
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def login(request):
    print "xxxx"
    if request.method == "GET":
        return render(request, "terminalUser/terminal_login.html", {})
    else:
        try:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            print username, password
            if username is None or password is None:
                return HttpResponse("error")
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    appuser = AppUser.objects.get(user=user)
                    print "check ok"
                    request.session['username'] = appuser.username
                    return HttpResponse("success")
                else:
                    print "not ok"
                    return HttpResponse("error")
            except Exception, e:
                print str(e)
                return HttpResponse("error")
        except Exception, e:
            print "Get Data"
            print(str(e))
            return HttpResponse("error")


@csrf_exempt
def update(request):
    try:
        user = AppUser.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect("/terminal/user/login/")
    try:
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        address = request.POST.get("address", None)
        telephone = request.POST.get("telephone", None)
        if password != "":
            password = make_password(password, None, 'pbkdf2_sha256')
            user.user.password = password
            user.user.save()
        user.email = email
        user.address = address
        user.telephone = telephone
        user.save()
        return HttpResponse("success")
    except Exception, e:
        print str(e)
        return HttpResponse("error")