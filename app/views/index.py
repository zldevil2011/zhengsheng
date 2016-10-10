# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Adminer
from django.contrib.auth.hashers import check_password


@csrf_exempt
def admin_index(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_index.html', {
        "user" : user,
    })


def admin_login(request):
    return render(request, 'app/admin_login.html', {})