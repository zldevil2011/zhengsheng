#coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from app.models import AppUser, Data, Device
from dss.Serializer import serializer
from django.contrib.auth.hashers import check_password
import math
import sys
from datetime import datetime, timedelta
import time
import json


def index(request):
	print(request.session['username'])
	try:
		user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	device = user.device
	# 获取当前用户今日的各类数据（按照采集时间）：用电量，电压，电流，温度
	today = datetime.today()
	today = datetime(today.year, today.month, today.day, 0, 0)
	datas = Data.objects.filter(device_id=device, date_time__gte=today)
	datas = serializer(datas)
	data_list = []
	for data in datas:
		try:
			data["tempT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempT"])))
		except Exception as e:
			print(str(e))
		try:
			data["powerT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["powerT"])))
		except Exception as e:
			print(str(e))
		try:
			data["tempBT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempBT"])))
		except Exception as e:
			print(str(e))
		try:
			# data["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["date_time"])))
			data["date_time"] = 1000 * int(data["date_time"])
		except Exception as e:
			print(str(e))
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
	try:
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
	except:
		pass
	return render(request, "phone/index.html", {
		"ret_data_dic":ret_data_dic,
		"device":device,
		"user":user,
	})


def historical(request):
	try:
		user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	device = user.device
	# 获取当前用户历史采集日期的的各类数据（按照采集时间）：用电量，电压，电流，温度
	try:
		start_filter_time = datetime.strptime(request.GET.get("start_filter_time"), "%Y-%m-%d")
		end_filter_time = datetime.strptime(request.GET.get("end_filter_time"), "%Y-%m-%d")
		start_filter_time = datetime(start_filter_time.year, start_filter_time.month, start_filter_time.day, 0, 0)
		end_filter_time = datetime(end_filter_time.year, end_filter_time.month, end_filter_time.day, 0, 0)
	except Exception as e:
		print(str(e))
		start_filter_time = datetime.today()
		start_filter_time = datetime(start_filter_time.year, start_filter_time.month, start_filter_time.day, 0, 0)
		end_filter_time = start_filter_time + timedelta(days=1)
	print start_filter_time
	print end_filter_time
	try:
		datas = Data.objects.filter(device_id=device, date_time__gte=start_filter_time, date_time__lte=end_filter_time)
		datas = serializer(datas)
		data_list = []
		for data in datas:
			try:
				data["tempT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempT"])))
			except Exception as e:
				print(str(e))
			try:
				data["powerT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["powerT"])))
			except Exception as e:
				print(str(e))
			try:
				data["tempBT"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["tempBT"])))
			except Exception as e:
				print(str(e))
			try:
				# data["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["date_time"])))
				data["date_time"] = 1000 * int(data["date_time"])
			except Exception as e:
				print(str(e))

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
				ret_power.append(datas[idx]["powerV"] - datas[idx - 1]["powerV"])
		device = serializer(device)
		device["todayPower"] = datas[len(datas) - 1]["powerV"] - datas[0]["powerV"]
		device["voltage"] = datas[len(datas) - 1]["voltage"]
		device["electric_current"] = datas[len(datas) - 1]["electric_current"]
		ret_data_dic = {}
		ret_data_dic["ret_power"] = ret_power
		ret_data_dic["ret_electricity"] = ret_electricity
		ret_data_dic["ret_voltage"] = ret_voltage
		ret_data_dic["ret_temperature"] = ret_temperature
		ret_data_dic["ret_time"] = ret_time
		ret_data_dic["device"] = device
		ret_data_dic = json.dumps(ret_data_dic)
		print ret_data_dic
	except:
		device = serializer(device)
		ret_data_dic = {}
		ret_data_dic["ret_power"] = []
		ret_data_dic["ret_electricity"] = []
		ret_data_dic["ret_voltage"] = []
		ret_data_dic["ret_temperature"] = []
		ret_data_dic["ret_time"] = []
		ret_data_dic["device"] = device
		ret_data_dic = json.dumps(ret_data_dic)
	return render(request, "phone/historicalData.html", {
		"ret_data_dic": ret_data_dic,
		"device": device,
		"user": user,
	})


def information_details(request):
	try:
		user = AppUser.objects.get(username=request.session['username'])
	except:
		return HttpResponseRedirect("/phone/user/login/")
	device = user.device
	# 获取当前用户今日的各类数据（小时级别）：用电量，电压，电流，温度
	try:
		today = datetime.today()
		hour = today.hour
		today_start = datetime(today.year, today.month, today.day, 0, 0)
		datas = Data.objects.filter(device_id=device, date_time__gte=today_start)
		print datas
		first_data = datas[0]
		# datas = serializer(datas)
		data_list = []
		tmp = {}
		tmp["time"] = first_data.date_time.hour
		tmp["power"] = first_data.powerV
		tmp["totalPower"] = first_data.powerV
		tmp["temperature"] = first_data.temp
		tmp["status"] = device.device_status
		data_list.append(tmp)
		idx = 0
		print first_data.date_time.hour, hour
		for i in range(first_data.date_time.hour+1, hour):
			idx += 1
			time_now = datetime(today.year, today.month, today.day, i, 0)
			try:
				tmp_data = datas.filter(date_time__gte=time_now).order_by('-date_time')[0]
				print tmp_data
				tmp = {}
				tmp["time"] = i
				tmp["power"] = float(tmp_data.powerV) - data_list[idx-1]["power"]
				tmp["totalPower"] = tmp_data.powerV
				tmp["temperature"] = tmp_data.temp
				tmp["status"] = device.device_status
				data_list.append(tmp)
			except:
				pass
		data_list[0]["power"] = 0
	except Exception as e:
		print(str(e))
		data_list = []
		pass
	print data_list
	return render(request, "phone/informationDetails.html", {
		"device": device,
		"user": user,
		"data_list": data_list,
	})