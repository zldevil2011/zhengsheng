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
        try:
            user_id = request.GET.get("user_id")
            print(user_id)
            user = AppUser.objects.get(pk=int(user_id))
            work_order_list = WorkOrder.objects.filter(appuser=user).order_by('-time')
            serializer = WorkOrderSerializer(work_order_list, many=True)
            return Response({'workOrderList':serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)