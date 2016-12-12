# coding=utf-8
from rest_framework import status
from django.contrib.auth.models import User
from app.models import AppUser, Data, Feedback
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import AppUserSerializer
from django.contrib.auth.hashers import check_password,make_password
from datetime import date, datetime, timedelta
import calendar

class FeedbackAdd(APIView):

    def post(self, request, format=None):
        try:
            user_id = int(request.data['user_id'])
            appuser = AppUser.objects.get(pk=user_id)
            content = request.data['content']
            email = appuser.user.email
            feedback = Feedback()
            feedback.email = email
            feedback.content = content
            feedback.save()
            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            print(str(e))
            return Response(status=status.HTTP_403_FORBIDDEN)