# coding=utf-8
from rest_framework import status
from django.contrib.auth.models import User
from app.models import AppUser, Data, Feedback, WorkOrder
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import WorkOrderSerializer
from django.contrib.auth.hashers import check_password,make_password
from datetime import date, datetime, timedelta
import calendar


class UserWorkOrder(APIView):

    def get(self, request, format=None):
        try:
            user_id = int(request.GET.get('user_id', 0))
            appuser = AppUser.objects.get(pk=user_id)
            work_order_list = WorkOrder.objects.filter(appuser=appuser)
            serializer = WorkOrderSerializer(work_order_list)
            return Response({'work_order_list': serializer.data}, status=status.HTTP_200_OK)
        except Exception, e:
            print(str(e))
            return Response(status=status.HTTP_403_FORBIDDEN)