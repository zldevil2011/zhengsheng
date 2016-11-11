# coding=utf-8
from rest_framework import status
from app.models import Event, Device
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from datetime import datetime

class EventUpload(APIView):

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
                        elif key == "evenT":
                            event.time = datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
                        elif key == "eventC":
                            event.content = val
                        else:
                            pass
                    device = Device.objects.get(device_id=device_id)
                    event.device = device
                    event.save()
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
