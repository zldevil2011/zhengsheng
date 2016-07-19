
# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


@csrf_exempt
def admin_app_user(request):
    return render(request, 'app/admin_appUser.html', {})


def admin_app_download(request):
    return render(request, 'app/admin_appDownload.html', {})


