# coding=utf-8
from rest_framework import status
from app.models import AppUser, Data, WorkOrder
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer
from datetime import date, datetime, timedelta
import calendar

class UserInfo(APIView):
    def get(self, request, format=None):
        user_id = int(request.GET.get('user_id', 0))
        try:
            user = AppUser.objects.get(pk=user_id)
            serializer = AppUserSerializer(user)
            return Response({'user':serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        print request.data
        try:
            user_id = int(request.data['user_id'])
            username = request.data['username']
            telephone = request.data['telephone']
            email = request.data['email']
            address = request.data['address']
            user = AppUser.objects.get(pk=user_id)
            user.user.email = email
            user.user.save()
            user.username = username
            user.telephone = telephone
            user.address = address
            user.email = email
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)