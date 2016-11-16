# coding=utf-8
from rest_framework import status
from app.models import Device, Parameter
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time

class DeviceParameter(APIView):

    def post(self, request, format=None):
        request_str = request.data['k']
        request_list = request_str.split(',')
        device_id = request_list[0].split("=")[1]
        ver_no = int(request_list[1].split("=")[1])
        try:
            device = Device.objects.get(device_id = device_id)
            parameter = Parameter.objects.get(device=device)
            up = '1'
            if parameter.version <= ver_no:
                up = '0'
            else:
                up = '1'

            parVer=parameter.version
            TempSet = int(parameter.temperature * 100)
            TempTSet = parameter.temperature_t_length
            PUTime1 = parameter.power_get_point1
            PUTime2 = parameter.power_get_point2
            response_str = ''
            response_str += 'up=' + up + ',id=' + str(device_id) + ',parVer=' + str(parVer) + ',TempSet=' + str(TempSet) + ',TempTSet='+str(TempTSet)+',PUTime1='+str(PUTime1)+',PUTime2='+str(PUTime2)
            return Response({'k': response_str} , status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            request_str = request.data['k']
            request_list = request_str.split(',')
            device_id = int(request_list[0].split("=")[1])
            device = Device.objects.get(device_id=device_id)
            parameter = Parameter()
            parameter.device = device
            parameter.temperature_t_length = 0
            parameter.temperature = 0
            parameter.power_get_point1 = '00:00:00'
            parameter.power_get_point2 = '12:00:00'
            parameter.version = 1
            parameter.save()
            response_str = 'up=1,id=' + str(device_id) + ',parVer=1,TempSet=0,TempTSet=0,PUTime1=00:00:00,PUTime2=12:00:00'
            return Response({'k': response_str} , status=status.HTTP_200_OK)
