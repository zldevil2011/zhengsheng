#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.terminalView import index, month_fees
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="terminalUser/base.html")),
    url(r'electricity_info/$', TemplateView.as_view(template_name="terminalUser/terminal_electricity_info.html")),
    url(r'fees/$', TemplateView.as_view(template_name="terminalUser/terminal_fees.html")),
    url(r'details/$', TemplateView.as_view(template_name="terminalUser/terminal_details.html")),
    url(r'month/$', month_fees.index, name="month_fees"),
    url(r'index/$', index.index, name="terminal-index"),
]