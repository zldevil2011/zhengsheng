# coding=utf-8
__author__ = 'kdq'
from django.conf.urls import url
from user.user_info import UserInfo
from device.device_check import DeviceCheck
from device.device_extramessage import DeviceExtramessage
from device.device_uploaddata import DeviceUploadData
from device.device_parameter import DeviceParameter

urlpatterns = [
    url('^user_info/', UserInfo.as_view()),
    url('^device/check/', DeviceCheck.as_view()),
    url('^device/extramessage/', DeviceExtramessage.as_view()),
    url('^device/data/', DeviceUploadData.as_view()),
    url('^device/parameter/', DeviceParameter.as_view())
]