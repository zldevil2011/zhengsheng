# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Adminer
from django.contrib.auth.hashers import check_password
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@csrf_exempt
def login(request):
	if request.method == "GET":
		return render(request, "phone/login.html", {

		})
	else:
		# return HttpResponse("error")
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		print username, password
		try:
			try:
				appuser = AppUser.objects.get(username=username)
				user = appuser.user
				print check_password(password, user.password)
				if check_password(password, user.password):
					print "check ok"
					request.session['username'] = appuser.username
					return HttpResponse("success")
				else:
					return HttpResponse("error")
			except Exception, e:
				return HttpResponse("error")
		except:
			return HttpResponse("error")


@csrf_exempt
def logout(request):
	try:
		user = Adminer.objects.get(name=request.session['username'])
	except:
		return HttpResponseRedirect("/admin_login/")
	del request.session['username']
	return HttpResponseRedirect("/admin_login/")