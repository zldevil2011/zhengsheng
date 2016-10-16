# coding=utf-8
from rest_framework import status
from app.models import AppUser, Data, WorkOrder
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer, WorkOrderSerializer
from datetime import date, datetime, timedelta
import calendar

class workOrderList(APIView):
    def get(self, request, format=None):
        print request.GET
        user_id = request.GET.get("user_id")
        print(user_id)
        user = AppUser.objects.get(pk=int(user_id))
        work_order_list = WorkOrder.objects.filter(appuser=user).order_by('-time')
        serializer = WorkOrderSerializer(work_order_list, many=True)
        return Response({'workOrderList':serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        print request.data
        user_id = int(request.data['user_id'])
        user = AppUser.objects.get(pk=user_id)
        device = user.device


        return Response({'month_data': month_data, 'today_data': today_data, 'workorder_len': workorder_len, 'tempalert_len': tempalert_len}, status=status.HTTP_200_OK)