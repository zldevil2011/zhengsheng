# coding=utf-8
__author__ = 'kdq'
from django.conf.urls import url
from user.user_info import UserInfo
from device.device_check import DeviceCheck

urlpatterns = [
    url('^user_info/', UserInfo.as_view()),
    url('^device/check/', DeviceCheck.as_view())
]