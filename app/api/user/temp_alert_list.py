# coding=utf-8
from rest_framework import status
from app.models import AppUser, Data, WorkOrder
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DataSerializer
from datetime import date, datetime, timedelta
import calendar


class tempAlertList(APIView):
    def get(self, request, format=None):
        print request.GET
        try:
            user_id = request.GET.get("user_id")
            print(user_id)
            user = AppUser.objects.get(pk=int(user_id))
            device = user.device
            temp_alert_list = Data.objects.filter(device_id=device, tempB=1).order_by('-tempBT')
            serializer = DataSerializer(temp_alert_list, many=True)
            return Response({'tempAlertList':serializer.data}, status=status.HTTP_200_OK)
        except Exception, e:
            print(str(e))
            return Response(status=status.HTTP_403_FORBIDDEN)