# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


@csrf_exempt
def admin_index(request):
    return render(request, 'app/admin_index.html', {})


def admin_login(request):
    return render(request, 'app/admin_login.html', {})