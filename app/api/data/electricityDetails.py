# coding=utf-8
from rest_framework import status
from app.models import AppUser, Data, WorkOrder
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer
from datetime import date, datetime, timedelta
import time
import calendar

class electricityDetails(APIView):

    def post(self, request, format=None):
        print request.data
        user_id = int(request.data['user_id'])
        user = AppUser.objects.get(pk=user_id)
        device = user.device
        today = date.today()
        year = today.year
        month = today.month
        day = today.day
        # 获取电压有效值
        voltage_data = {}
        voltage_x = []
        voltage_y = []
        try:
            datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month,
                                                   powerT__day=day).order_by('-date_time')
            datas_list_today.reverse()
            for data in datas_list_today:
                voltage_x.append(int(time.mktime(data.date_time)))
                voltage_y.append(data.voltage)
        except:
            datas_list_today = None
        voltage_data["voltage_x"] = voltage_x
        voltage_data["voltage_y"] = voltage_y
        # 获取电流有效值
        electric_current_data = {}
        electric_current_x = []
        electric_current_y = []
        try:
            datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month,
                                                   powerT__day=day).order_by('-date_time')
            datas_list_today.reverse()
            for data in datas_list_today:
                electric_current_x.append(int(time.mktime(data.date_time)))
                electric_current_y.append(data.electric_current)
        except:
            datas_list_today = None
        electric_current_data["electric_current_x"] = electric_current_x
        electric_current_data["electric_current_y"] = electric_current_y
        # 获取功率因数
        power_factor_data = {}
        power_factor_x = []
        power_factor_y = []
        try:
            datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month,
                                                   powerT__day=day).order_by('-date_time')
            datas_list_today.reverse()
            for data in datas_list_today:
                power_factor_x.append(int(time.mktime(data.date_time)))
                power_factor_y.append(data.power_factor)
        except:
            datas_list_today = None
        power_factor_data["power_factor_x"] = power_factor_x
        power_factor_data["power_factor_y"] = power_factor_y
        # 获取有功功率
        active_power_data = {}
        active_power_x = []
        active_power_y = []
        try:
            datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month,
                                                   powerT__day=day).order_by('-date_time')
            datas_list_today.reverse()
            for data in datas_list_today:
                active_power_x.append(int(time.mktime(data.date_time)))
                active_power_y.append(data.active_power)
        except:
            datas_list_today = None
        active_power_data["active_power_x"] = active_power_x
        active_power_data["active_power_y"] = active_power_y
        # 获取无功功率
        reactive_power_data = {}
        reactive_power_x = []
        reactive_power_y = []
        try:
            datas_list_today = Data.objects.filter(device_id=device, powerT__year=year, powerT__month=month,
                                                   powerT__day=day).order_by('-date_time')
            datas_list_today.reverse()
            for data in datas_list_today:
                reactive_power_x.append(int(time.mktime(data.date_time)))
                reactive_power_y.append(data.reactive_power)
        except:
            datas_list_today = None
        reactive_power_data["reactive_power_x"] = reactive_power_x
        reactive_power_data["reactive_power_y"] = reactive_power_y

        return Response({'voltage_data': voltage_data, 'electric_current_data': electric_current_data,
                         'power_factor_data': power_factor_data, 'active_power_data': active_power_data,
                         'reactive_power_data':reactive_power_data}, status=status.HTTP_200_OK)