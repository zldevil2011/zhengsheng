# coding=utf-8
from rest_framework import status
from app.models import AppUser, Data, WorkOrder,Event
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import DataSerializer, EventSerializer
from datetime import date, datetime, timedelta
import calendar


class NewsList(APIView):
    def get(self, request, format=None):
        print request.GET
        file_object = open('test.txt')
        news_data = []
        list_of_all_the_lines = file_object.readlines()
        file_object.close()
        # print list_of_all_the_lines
        idx = 0
        while idx <= (len(list_of_all_the_lines) - 3):
            tmp = {}
            tmp["link"] = list_of_all_the_lines[idx][:-1]
            tmp["name"] = list_of_all_the_lines[idx + 1][:-1].decode('gb2312')
            tmp["img"] = list_of_all_the_lines[idx + 2][:-1]
            news_data.append(tmp)
            idx += 3
        print news_data
        return Response({"news_list": news_data}, , status=status.HTTP_200_OK)

