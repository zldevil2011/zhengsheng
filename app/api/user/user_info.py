# coding=utf-8
from rest_framework import status
from app.models import AppUser
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer


class UserInfo(APIView):
    def get(self, request, format=None):
        user = AppUser.objects.get(pk=1)
        serializer = AppUserSerializer(user)
        return Response({'user':serializer.data}, status=status.HTTP_200_OK)
