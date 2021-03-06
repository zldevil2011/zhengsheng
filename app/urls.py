#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import index, user, device, data, mobile, installArea, admin_info,workOrder, event
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="app/welcome.html")),
    # 管理图像
    url(r'^building/$', TemplateView.as_view(template_name="app/building.html")),
    # 管理员登陆
    url(r'^admin_login/$', index.admin_login, name="admin_login"),
    # 管理首页
    url(r'^admin_index/$', index.admin_index, name="admin_index"),
    # 获取最新的十条温度报警
    url(r'^admin_get_latest_warning_event/$', index.latest_event, name="latest_event"),
    url(r'^admin_index/$', index.admin_index, name="admin_index"),
    # 账户管理
    url(r'^admin_account/$', user.admin_account, name="admin_account"),
    url(r'^admin_account/delete/$', user.admin_delete_user, name="delete_user"),
    # 工单管理
    url(r'^admin_work_order/$', workOrder.index, name="admin_work_order"),
    url(r'^admin_work_order/(?P<wo_id>\d+)/$', workOrder.info, name="admin_work_order_info"),
    url(r'^admin_work_order/query/$', workOrder.work_order_filter, name="work_order_filter"),
    # 设备管理
    url(r'^admin_device/$', device.admin_device, name="admin_device"),
    url(r'^admin_device/filter/$', device.admin_device_filter, name="admin_device_filter"),
        # 设备添加
    url(r'^admin_device/add/$', device.admin_device_add, name="admin_device_add"),
        # 设备移除
    url(r'^admin_device/remove/$', device.admin_device_remove, name="admin_device_remove"),
        # 设备定位
    url(r'^admin_device/location/$', device.admin_device_location, name="admin_device_location"),

    url(r'^admin_device/maintain/$', device.admin_device_maintain, name="admin_device_maintain"),
    url(r'^admin_device/maintain/filter/$', device.admin_device_maintain_filter, name="admin_device_maintain_filter"),

    url(r'^admin_device/temperature/$', device.admin_device_temperature, name="admin_device_temperature"),

    url(r'^admin_device/health/$', device.admin_device_health, name="admin_device_health"),

    url(r'^admin_device/leakage/$', device.admin_device_leakage, name="admin_device_leakage"),

    url(r'^admin_device/(?P<device_id>\d+)/$', device.admin_device_info, name="admin_device_info"),

    # 网关参数设定
    url(r'^admin_device/gateway/parameter/$', device.admin_device_gateway_parameter, name="admin_device_gateway_parameter"),
    # 数据查看
    url(r'^admin_data/$', data.admin_data, name="admin_data"),
    # 查看某个用户的设备数据
    url(r'^admin_data/userinfo/$', data.admin_user_data, name="admin_user_data"),

    url(r'^admin_mobile/user/$', mobile.admin_mobile_user, name="admin_mobile_user"),

    url(r'^admin_mobile/download/$', mobile.admin_mobile_download, name="admin_mobile_download"),

    url(r'^admin_user/login/$', user.login, name="login"),

    url(r'^admin_user/logout/$', user.logout, name="logout"),
    # 区域管理
    url(r'^admin_area/list/$', installArea.area_list, name="area_list"),
    url(r'^admin_area/city/add/$', installArea.city_add, name="city_add"),
    url(r'^admin_area/city/delete/$', installArea.city_delete, name="city_delete"),

    url(r'^admin_area/village/add/$', installArea.village_add, name="village_add"),
    url(r'^admin_area/city/village_list/$', installArea.city_village_list, name="city_village_list"),
    url(r'^admin_area/city/delete/$', installArea.village_delete, name="village_delete"),
    # 管理员信息列表
    url(r'^admin_info/user/$', admin_info.user, name="admin_info_user"),
    url(r'^admin_info/user/sendMail/$', admin_info.sendMail, name="sendMail"),
    # 事件管理
    url(r'^admin_event/$', event.admin_event, name="admin_event"),
    url(r'^admin_event/user/sendMail/$', event.user_send_mail, name="user_send_mail"),
    # 中继数据管理
    url(r'^admin_relay/data/$', device.admin_relay_data, name="admin_relay")
]
urlpatterns += {
    url(r'^device/list/$', device.list, name="device_list"),
    url(r'^device/instock/$', device.instock, name="device_instock"),
    url(r'^device/info/$', device.device_info, name="device_info"),

    url(r'^contactUs$', TemplateView.as_view(template_name="app/contactUs.html")),
}