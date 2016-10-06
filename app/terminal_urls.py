#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.terminalView import index, month_fees, user_work_order, user, power, device, fund, details
urlpatterns = [
    # url(r'/$', TemplateView.as_view(template_name="terminalUser/terminal_login.html")),

    # url(r'login/$', TemplateView.as_view(template_name="terminalUser/terminal_login.html")),
    url(r'user/login/$', user.login, name="terminal-user-login"),
    url(r'user/update/$', user.update, name="terminal-user-update"),

    url(r'index/$', index.index, name="terminal-index"),

    url(r'electricity_info/$', power.electricity_info, name = "electricity_info"),

    url(r'device_info/$', device.terminal_device_info, name="terminal_device_info"),

    url(r'fund/$', fund.index, name="fund_index"),

    url(r'details/$', details.index, name="details_index"),

    url(r'month/$', month_fees.index, name="month_fees"),

    url(r'work_order/$', user_work_order.index, name="work_order"),
    url(r'work_order/(?P<wo_id>\d+)/$', user_work_order.info, name="work_order"),
    url(r'work_order/add/$', user_work_order.add_work_order, name="add_work_order"),
]