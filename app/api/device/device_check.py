# coding=utf-8
from rest_framework import status
from app.models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time

class DeviceCheck(APIView):

    def post(self, request, format=None):
        print request.data
        # return Response({"k":"123"}, status=status.HTTP_200_OK)
        request_str = request.data['k']
        request_val_list = request_str.split('=')
        print request_val_list
        device_id = int(request_val_list[1])
        print "device_id = ", device_id
        # comment_content = request.data['comment_content']
        timeF = '%Y-%m-%d %X'
        CurTime = time.strftime(timeF, time.localtime())
        try:
            device = Device.objects.get(device_id = device_id)
            ext_info = '0'
            if device.city_code is None or device.village_code is None or device.gateway_code is None:
                ext_info = '1'
            response_str = ''
            response_str += 'valid_s=1/CurTime='+CurTime+'/ext_info='+ext_info
            return Response({'k': response_str} , status=status.HTTP_200_OK)
        except:
            response_str = ''
            response_str += 'valid_s=0/CurTime=' + CurTime + '/ext_info=1'
            return Response({'k': response_str}, status=status.HTTP_200_OK)
