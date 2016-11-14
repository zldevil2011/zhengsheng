# coding=utf-8
from rest_framework import status
from app.models import Device, Data, Relay
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time
from datetime import datetime


def checkInfo(request, device_id):
    device = Device.objects.get(device_id)
    if device.city_code is None or device.village_code is None or device.building_code is None or device.unit_code is None or device.room_code is None:
        return 1
    return 0


class DeviceUploadData(APIView):

    def post(self, request, format=None):
        try:
            request_str = request.data['k']
            device_list = request_str.split('/')
            print device_list
            InvID = []
            ExtInfoID = []
            for device in device_list:
                device_data_list = device.split(',')
                print device_data_list
                try:
                    device_id = int(device_data_list[0].split('=')[1])
                    device = Device.objects.get(device_id=device_id)
                    if device_id < 200000000 or device_id >= 300000000:
                        new_data = Data()
                        new_data.device_id = device
                        for data in device_data_list:
                            key = data.split('=')[0].strip()
                            val = data.split('=')[1].strip()
                            print key, ":", val
                            now = datetime.today()
                            now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
                            if key == "temp":
                                new_data.temp = float(val)
                                # new_data.tempT = now
                            elif key == "tempT":
                                new_data.tempT = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            elif key == "powerV":
                                new_data.powerV = float(val)
                                # new_data.powerT = now
                            elif key == "powerI":
                                new_data.powerI = float(val)
                                # new_data.powerT = now
                            elif key == "powerT":
                                new_data.powerT = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            elif key == "tempB":
                                new_data.tempB = int(val)
                                # new_data.tempBT = now
                            elif key == "tempBT":
                                new_data.tempBT = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            elif key == "faultB":
                                new_data.faultB = int(val)
                                # new_data.faultBT = now
                            elif key == "faultBT":
                                new_data.faultBT = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            elif key == "vol":
                                new_data.voltage = float(val)/10.0
                            elif key == "elec":
                                new_data.electric_current = float(val)/10.0
                            elif key == "powerF":
                                new_data.power_factor = float(val)/1000.0
                            elif key == "powerA":
                                new_data.active_power = float(val)
                            elif key == "powerR":
                                new_data.reactive_power = float(val)
                            elif key == "time":
                                new_data.date_time = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            else:
                                pass
                        new_data.save()
                    else:
                        relay = Relay()
                        relay.device_id = device
                        for data in device_data_list:
                            key = data.split('=')[0].strip()
                            val = data.split('=')[1].strip()
                            print key, ":", val
                            if key == "a_vol":
                                relay.a_voltage = float(val)/10.0
                            elif key == "b_vol":
                                relay.b_voltage = float(val)/10.0
                            elif key == "c_vol":
                                relay.c_voltage = float(val)/10.0
                            elif key == "a_elec":
                                relay.a_electric_current = float(val)/10.0
                            elif key == "b_elec":
                                relay.b_electric_current = float(val)/10.0
                            elif key == "c_elec":
                                relay.c_electric_current = float(val)/10.0
                            elif key == "a_powerF":
                                relay.a_power_factor = float(val)/1000.0
                            elif key == "b_powerF":
                                relay.b_power_factor = float(val)/1000.0
                            elif key == "c_powerF":
                                relay.c_power_factor = float(val)/1000.0
                            elif key == "a_powerA":
                                relay.a_active_power = float(val)
                            elif key == "b_powerA":
                                relay.b_active_power = float(val)
                            elif key == "c_powerA":
                                relay.c_active_power = float(val)
                            elif key == "a_powerR":
                                relay.a_reactive_power = float(val)
                            elif key == "b_powerR":
                                relay.b_reactive_power = float(val)
                            elif key == "c_powerR":
                                relay.c_reactive_power = float(val)
                            elif key == "a_powerV":
                                relay.a_powerV = float(val)
                            elif key == "b_powerV":
                                relay.b_powerV = float(val)
                            elif key == "c_powerV":
                                relay.c_powerV = float(val)
                            elif key == "a_powerI":
                                relay.a_powerI = float(val)
                            elif key == "b_powerI":
                                relay.b_powerI = float(val)
                            elif key == "c_powerI":
                                relay.c_powerI = float(val)
                            elif key == "t_powerV":
                                relay.t_powerV = float(val)
                            elif key == "t_powerI":
                                relay.t_powerI = float(val)
                            elif key == "time":
                                relay.data_time = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                            else:
                                pass
                            relay.save()
                    if device_id < 200000000:
                        if device.city_code is None or device.village_code is None or device.building_code is None or device.unit_code is None or device.room_code is None:
                            ExtInfoID.append(device_id)
                    elif device_id < 300000000:
                        if device.city_code is None or device.village_code is None or device.building_code is None or device.unit_code is None:
                            ExtInfoID.append(device_id)
                    else:
                        if device.city_code is None or device.village_code is None:
                            ExtInfoID.append(device_id)
                except Exception, e:
                    print str(e)
                    device_id = int(device_data_list[0].split('=')[1])
                    print "failed = " + str(device_id)
                    InvID.append(str(device_id))
            response_str = ''
            for inv in InvID:
                response_str += "InvID=" + str(inv) + "/"
            for ext in ExtInfoID:
                response_str += "ExtInfoID=" + str(ext) + "/"
            # response_str = response_str.remove(len(response_str) - 1)
            # print "res_str = " + request_str
            print(response_str)
            return Response({'k': response_str}, status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            request_str = request.data['k']
            device_list = request_str.split('/')
            print device_list
            InvID = []
            ExtInfoID = []
            for device in device_list:
                device_data_list = device.split(',')
                print device_data_list
                device_id = int(device_data_list[0].split('=')[1])
                InvID.append(device_id)
            response_str = ''
            for inv in InvID:
                response_str += "InvID=" + str(inv) + "/"
            return Response({'k': response_str}, status=status.HTTP_200_OK)
