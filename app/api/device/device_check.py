# coding=utf-8
from rest_framework import status
from app.models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time

class DeviceCheck(APIView):

    def post(self, request, format=None):
        device_id = int(request.data.get('id', 0))
        print "device_id = ", device_id
        # comment_content = request.data['comment_content']
        timeF = '%Y-%m-%d %X'
        CurTime = time.strftime(timeF, time.localtime())
        try:
            device = Device.objects.get(device_id = device_id)
            ext_info = 0
            if device.city_code is None or device.village_code is None or device.gateway_code is None:
                ext_info = 1
            return Response({'valid_s': 1, 'CurTime': CurTime, 'ext_info': ext_info},status=status.HTTP_200_OK)
        except:
            return Response({'valid_s': 0, 'CurTime':CurTime, 'ext_info': '1'}, status=status.HTTP_404_NOT_FOUND)
