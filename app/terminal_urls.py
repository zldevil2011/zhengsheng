#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import index, user, device, data, mobile, installArea, admin_info
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="terminalUser/base.html")),
]