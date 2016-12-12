# coding=utf-8
__author__ = 'zhaolong'
from django.conf.urls import url
from user.user_info import UserInfo
from user.login import Login
from user.work_order_list import workOrderList
from user.temp_alert_list import tempAlertList
from user.feedback_add import FeedbackAdd
from user.event_list import EventList
from device.device_check import DeviceCheck
from device.device_extramessage import DeviceExtramessage
from device.device_uploaddata import DeviceUploadData
from device.device_parameter import DeviceParameter
from event.event_upload import EventUpload
from data.electricityInfo import electricityData
from data.electricityDetails import electricityDetails

urlpatterns = [
    url('^user_info/', UserInfo.as_view()),
    url('^user/login/', Login.as_view()),
    url('^user/workorderList/', workOrderList.as_view()),
    url('^user/tempAlertList/', tempAlertList.as_view()),
    url('^user/eventList/', EventList.as_view()),
    url('^user/electricity/data/', electricityData.as_view()),
    url('^user/electricity/details/', electricityDetails.as_view()),

    url('^feedback_add/', FeedbackAdd.as_view()),


    url('^device/check/', DeviceCheck.as_view()),
    url('^device/extramessage/', DeviceExtramessage.as_view()),
    url('^device/data/', DeviceUploadData.as_view()),
    url('^device/parameter/', DeviceParameter.as_view()),
    url('^event_add/', EventUpload.as_view())
]