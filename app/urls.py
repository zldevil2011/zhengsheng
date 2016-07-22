#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import index, user, device, data, mobile, installArea
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="app/welcome.html")),
    url(r'^building/$', TemplateView.as_view(template_name="app/building.html")),
    url(r'^admin_login/$', index.admin_login, name="admin_login"),
    url(r'^admin_index/$', index.admin_index, name="admin_index"),
    url(r'^admin_account/$', user.admin_account, name="admin_account"),
    url(r'^admin_work_order/$', user.admin_work_order, name="admin_work_order"),
    url(r'^admin_device/$', device.admin_device, name="admin_device"),
    url(r'^admin_device/add/$', device.admin_device_add, name="admin_device_add"),
    url(r'^admin_device/remove/$', device.admin_device_remove, name="admin_device_remove"),
    url(r'^admin_device/location/$', device.admin_device_location, name="admin_device_location"),
    url(r'^admin_device/maintain/$', device.admin_device_maintain, name="admin_device_maintain"),
    url(r'^admin_device/temperature/$', device.admin_device_temperature, name="admin_device_temperature"),
    url(r'^admin_device/health/$', device.admin_device_health, name="admin_device_health"),
    url(r'^admin_device/leakage/$', device.admin_device_leakage, name="admin_device_leakage"),
    url(r'^admin_data/$', data.admin_data, name="admin_data"),
    url(r'^admin_mobile/user/$', mobile.admin_mobile_user, name="admin_mobile_user"),
    url(r'^admin_mobile/download/$', mobile.admin_mobile_download, name="admin_mobile_download"),
    url(r'^admin_user/login/$', user.login, name="login"),
    url(r'^admin_user/logout/$', user.logout, name="logout"),
    url(r'^admin_area/list/$', installArea.area_list, name="area_list"),
]