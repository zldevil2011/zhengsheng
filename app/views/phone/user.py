# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from dss.Serializer import serializer
from app.models import AppUser, Adminer, WorkOrder, Event
from django.contrib.auth.hashers import check_password, make_password
import math
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def my_information(request):
	try:
		user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	return render(request, "phone/myInformation.html", {
		"user_id":user.pk,
	})

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
		user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	del request.session['username']
	return HttpResponseRedirect("/admin_login/")


@csrf_exempt
def personal(request):
	try:
		user_id = int(request.GET.get("user_id"))
		user = AppUser.objects.get(pk=user_id)
		# user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	if request.method == "GET":
		return render(request, "phone/personalInformation.html", {
			"user":user,
		})
	else:
		try:
			oldPwd = request.POST.get("oldPwd")
			try:
				print check_password(oldPwd, user.user.password)
				if check_password(oldPwd, user.user.password):
					address = request.POST.get("address")
					telephone = request.POST.get("telephone")
					email = request.POST.get("email")
					user.address = address
					user.telephone = telephone
					user.email = email
					user.save()
					newPwd = request.POST.get("newPwd", None)
					if newPwd is not None and len(newPwd):
						secret_password = make_password(newPwd, None, 'pbkdf2_sha256')
						user.user.password = secret_password
						user.user.save()
						return HttpResponse("更新个人信息及密码成功")
					else:
						pass
					return HttpResponse("更新个人信息成功")
				else:
					return HttpResponse("原始密码不正确")
			except Exception, e:
				return HttpResponse("密码或个人信息不正确")
		except Exception as e:
			return HttpResponse(str(e))

@csrf_exempt
def workorder(request):
	try:
		user_id = int(request.GET.get("user_id"))
		user = AppUser.objects.get(pk=user_id)
		# user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	if request.method == "GET":
		workorder_list = WorkOrder.objects.filter(appuser=user)
		workorder_list = serializer(workorder_list, foreign=True)
		for work in workorder_list:
			work["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(work["time"]))
		print workorder_list
		return render(request, "phone/workorder.html", {
			"workorder_list":workorder_list,
			"user": user,
		})
	else:
		pass

@csrf_exempt
def warning(request):
	try:
		user_id = int(request.GET.get("user_id"))
		user = AppUser.objects.get(pk=user_id)
		# user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	if request.method == "GET":
		warning_list = Event.objects.filter(device=user.device)
		warning_list = serializer(warning_list, foreign=True)
		for warning in warning_list:
			warning["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(warning["time"]))
		print warning_list
		return render(request, "phone/warning.html", {
			"warning_list":warning_list,
			"user": user,
		})
	else:
		pass