# coding=utf-8
from rest_framework import status
from app.models import Device, AppUser, User
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DeviceSerializer
import time
import string
import random
from django.contrib.auth.hashers import check_password,make_password
from datetime import datetime

dict = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
class DeviceExtramessage(APIView):

    def post(self, request, format=None):
        try:
            request_str = request.data['k']
            print request_str
            device_list = request_str.split('/')
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
                    try:
                        appuser = AppUser.objects.get(device=device)
                    except AppUser.DoesNotExist:
                        if device.device_id < 200000000:
                            print u"用户不存在，创建新用户"
                            device.device_status = u"正常"
                            device.save()
                            user = User()
                            while 1:
                                rand_username = string.join(random.sample(dict, 10)).replace(' ', '')
                                try:
                                    appuser = AppUser.objects.get(username=rand_username)
                                except AppUser.DoesNotExist:
                                    break
                            user.username = rand_username
                            password = '123456'
                            password = make_password(password, None, 'pbkdf2_sha256')
                            user.password = password
                            user.save()
                            appuser = AppUser()
                            appuser.user = user
                            appuser.username = rand_username
                            appuser.register_time = datetime.now()
                            appuser.password = '123456'
                            appuser.device = device
                            appuser.save()
                except:
                    device_id = int(device_attr_list[0].split('=')[1])
                    print "failed = " + str(device_id)
                    fail_id.append(str(device_id))
            response_str = ''
            for fid in fail_id:
                response_str += "fail_id=" + fid + "/"
            # response_str += 'fail_id=' + ";".join(fail_id)
            print "res_str = " + request_str
            return Response({'k': response_str} , status=status.HTTP_200_OK)
        except Exception, e:
            print str(e)
            request_str = request.data['k']
            print request_str
            device_list = request_str.split('/')
            print device_list
            fail_id = []
            for device in device_list:
                device_attr_list = device.split(',')
                print device_attr_list
                device_id = int(device_attr_list[0].split('=')[1])
                fail_id.append(device_id)
            response_str = ''
            for fid in fail_id:
                response_str += "fail_id=" + fid + "/"
            return Response({'k': response_str}, status=status.HTTP_200_OK)
