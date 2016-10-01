# coding=utf-8
from rest_framework import status
from app.models import Device, Data
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time
import datetime


def checkInfo(request, device_id):
    device = Device.objects.get(device_id)
    if device.city_code is None or device.village_code is None or device.building_code is None or device.unit_code is None or device.room_code is None:
        return 1
    return 0


class DeviceUploadData(APIView):

    def post(self, request, format=None):
        try:
            request_str = request.data['k']
            device_list = request_str.split(';')
            print device_list
            InvID = []
            ExtInfoID = []
            for device in device_list:
                device_data_list = device.split('&')
                print device_data_list
                try:
                    device_id = int(device_data_list[0].split('=')[1])
                    device = Device.objects.get(device_id=device_id)
                    new_data = Data()
                    new_data.device_id = device
                    for data in device_data_list:
                        key = data.split('=')[0].strip()
                        val = data.split('=')[1].strip()
                        print key, ":", val
                        if key == "temp":
                            new_data.temp = float(val)
                        elif key == "tempT":
                            new_data.tempT = datetime.datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        elif key == "powerV":
                            new_data.powerV = float(val)
                        elif key == "powerI":
                            new_data.powerI = float(val)
                        elif key == "powerT":
                            new_data.powerT = datetime.datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        elif key == "tempB":
                            new_data.tempB = int(val)
                        elif key == "tempBT":
                            new_data.tempBT = datetime.datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        elif key == "faultB":
                            new_data.faultB = int(val)
                        elif key == "faultBT":
                            new_data.faultBT = datetime.datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        else:
                            pass
                    new_data.save()
                    if device.city_code is None or device.village_code is None or device.building_code is None or device.unit_code is None or device.room_code is None:
                        ExtInfoID.append(device_id)
                except Exception, e:
                    print str(e)
                    device_id = int(device_data_list[0].split('=')[1])
                    print "failed = " + str(device_id)
                    InvID.append(str(device_id))
            response_str = ''
            for inv in InvID:
                response_str += "InvID=" + str(inv) + ";"
            for ext in ExtInfoID:
                response_str += "ExtInfoID=" + str(ext) + ";"
            # response_str = response_str.remove(len(response_str) - 1)
            # print "res_str = " + request_str
            return Response({'k': response_str}, status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            response_str = ''
            response_str += 'InvID=all'
            return Response({'k': response_str}, status=status.HTTP_200_OK)
