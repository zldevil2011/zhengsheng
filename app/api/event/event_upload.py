# coding=utf-8
from rest_framework import status
from app.models import Event, Device, City, Village
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from datetime import datetime
from django.core.mail import send_mail
from zhengsheng import settings

class EventUpload(APIView):

    def get_event_name(self, id):
        name_list = ["正常",
                     "上电", "掉电", "清零", "参数设置", "校时",
                     "通信故障","失压","失流","断相","功率因数越限",
                     "电压偏差越限","电压、电流不平衡越限","温度过限","A相失压","B相失压",
                     "C相失压","A相失流","B相失流","C相失流","A相功率因数越限",
                     "B相功率因数越限","C相功率因数越限","A相电压偏差越限","B相电压偏差越限","C相电压偏差越限",
                     "A相电压、电流不平衡越限","B相电压、电流不平衡越限","C相电压、电流不平衡越限"]
        return name_list[id]

    def post(self, request, format=None):
        try:
            request_str = request.data['k']
            event_list = request_str.split('/')
            print event_list
            InvID = []
            for event in event_list:
                event_data_list = event.split(',')
                print event_data_list
                try:
                    device_id = int(event_data_list[0].split('=')[1])
                    event = Event()
                    for data in event_data_list:
                        key = data.split('=')[0].strip()
                        val = data.split('=')[1].strip()
                        print key, ":", val
                        if key == "event":
                            event.name_no = int(val)
                            event.name = self.get_event_name(int(val))
                        elif key == "eventT":
                            now = datetime.now()
                            event.time = now
                            # event.time = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        elif key == "eventC":
                            event.content = val
                        else:
                            pass
                    device = Device.objects.get(device_id=device_id)
                    event.device = device
                    event.save()
                    try:
                        city = City.objects.get(city_code=int(device.city_code))
                        village = Village.objects.get(city=city, village_code=int(device.village_code))
                        try:
                            address = city.city_name + village.village_name + str(device.building_code) + u"号楼" + \
                                    str(device.unit_code) + u"单元" + str(device.room_code) + u"房间"
                        except:
                            address = city.city_name + village.village_name
                    except:
                        address = u"未安装"
                    subject = u"事件通知"
                    text_content = u"设备（ID:" + str(event.device.device_id) + u")在" + str(event.time) + u"发生了" + str(
                        event.name) + u"事件（设备地址：" + address +  u")，请您及时查看"
                    from_email = settings.EMAIL_HOST_USER
                    to = "34985488@qq.com"
                    try:
                        send_mail(subject, text_content, from_email, [to], fail_silently=False)
                    except:
                        pass


                except Exception, e:
                    print str(e)
                    event_id = int(event_data_list[0].split('=')[1])
                    print "failed = " + str(event_id)
                    InvID.append(str(event_id))
            response_str = ''
            for inv in InvID:
                response_str += "InvID=" + str(inv) + "/"
            print(response_str)
            return Response({'k': response_str}, status=status.HTTP_200_OK)
        except Exception, e:
            print "Total-", str(e)
            request_str = request.data['k']
            event_list = request_str.split('/')
            print event_list
            InvID = []
            for event in event_list:
                event_data_list = event.split(',')
                print event_data_list
                event_id = int(event_data_list[0].split('=')[1])
                InvID.append(event_id)
            response_str = ''
            for inv in InvID:
                response_str += "InvID=" + str(inv) + "/"
            return Response({'k': response_str}, status=status.HTTP_200_OK)
