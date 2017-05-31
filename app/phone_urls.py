#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views.phone.device import index, historical, information_details
from app.views.phone.user import login, personal,workorder
urlpatterns = [
    url(r'index/$', index, name="phone_index"),
    url(r'historical/$', historical, name="historical"),
    url(r'informationDetails/$', information_details, name="information_details"),
    url(r'myInformation/$', TemplateView.as_view(template_name="phone/myInformation.html")),
    url(r'personal/$', personal, name="personal"),
    url(r'workorder/$', workorder, name="workorder"),
    url(r'user/login/$', login, name="login"),
]