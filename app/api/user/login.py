# coding=utf-8
from rest_framework import status
from django.contrib.auth.models import User
from app.models import AppUser, Data
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer
from django.contrib.auth.hashers import check_password,make_password
from datetime import date, datetime, timedelta
import calendar

class Login(APIView):

    def post(self, request, format=None):
        print request.data
        try:
            username = request.data['username']
            password = request.data["password"]
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                print "check ok"
                serializer = AppUserSerializer(user)
                return Response({'user': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)