#coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from app.models import AppUser, Data, Device
from dss.Serializer import serializer
from django.contrib.auth.hashers import check_password
import math
import sys
from datetime import datetime
import time
import json


def index(request):
	# try:
	# 	user = AppUser.objects.get(username=request.session['username'])
	# except:
	# 	return HttpResponsePermanentRedirect("/phone/user/login/")
	user = AppUser.objects.get(username='zhengsheng')
	device = user.device
	# 获取当前用户今日的各类数据（按照采集时间）：用电量，电压，电流，温度
	today = datetime.today()
	today = datetime(today.year, today.month, today.day, 0, 0)
	datas = Data.objects.filter(device_id=device, date_time__gte=today)
	datas = serializer(datas)
	data_list = []
	for data in datas:
		data["tempT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempT"])))
		data["powerT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["powerT"])))
		data["tempBT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempBT"])))
		data["faultBT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["faultBT"])))
		# data["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["date_time"])))
		data["date_time"] = 1000 * int(data["date_time"])
	ret_data_dic = {}
	ret_power = []
	ret_electricity = []
	ret_voltage = []
	ret_temperature = []
	ret_time = []
	for idx, data in enumerate(datas):
		ret_time.append(data["date_time"])
		ret_electricity.append(data["electric_current"])
		ret_voltage.append(data["voltage"])
		ret_temperature.append(data["temp"])
		if idx == 0:
			ret_power.append(0)
		else:
			ret_power.append(datas[idx]["powerV"] - datas[idx-1]["powerV"])
	device = serializer(device)
	device["todayPower"] = datas[len(datas) - 1]["powerV"] - datas[0]["powerV"]
	device["voltage"] = datas[len(datas) - 1]["voltage"]
	device["electric_current"] = datas[len(datas) - 1]["electric_current"]
	ret_data_dic["ret_power"] = ret_power
	ret_data_dic["ret_electricity"] = ret_electricity
	ret_data_dic["ret_voltage"] = ret_voltage
	ret_data_dic["ret_temperature"] = ret_temperature
	ret_data_dic["ret_time"] = ret_time
	ret_data_dic["device"] = device
	ret_data_dic = json.dumps(ret_data_dic)
	return render(request, "phone/index.html", {
		"ret_data_dic":ret_data_dic,
		"device":device,
		"user":user,
	})