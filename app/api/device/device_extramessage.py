# coding=utf-8
from rest_framework import status
from app.models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time

class DeviceExtramessage(APIView):

    def post(self, request, format=None):
        try:
            request_str = request.data['k']
            device_list = request_str.split(';')
            print device_list
            fail_id = []
            for device in device_list:
                device_attr_list = device.split(',')
                print device_attr_list
                try:
                    device_id = int(device_attr_list[0].split('=')[1])
                    device = Device.objects.get(device_id=device_id)
                    for attr in device_attr_list:
                        key = attr.split('=')[0].strip()
                        val = attr.split('=')[1].strip()
                        print key, ":", val
                        if key == "cno":
                            device.city_code = int(val)
                        elif key == "vno":
                            device.village_code = int(val)
                        elif key == "dno":
                            device.gateway_code = int(val)
                        elif key == "bno":
                            device.building_code = int(val)
                        elif key == "uno":
                            device.unit_code = int(val)
                        elif key == "zno":
                            device.meter_box = int(val)
                        elif key == "rno":
                            device.room_code = int(val)
                        else:
                            pass
                    device.save()
                except:
                    device_id = int(device_attr_list[0].split('=')[1])
                    print "failed = " + str(device_id)
                    fail_id.append(str(device_id))
            response_str = ''
            for fid in fail_id:
                response_str += "fail_id=" + fid + ";"
            # response_str += 'fail_id=' + ";".join(fail_id)
            print "res_str = " + request_str
            return Response({'k': response_str} , status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            response_str = ''
            response_str += 'fail_id=all'
            return Response({'k': response_str}, status=status.HTTP_200_OK)
