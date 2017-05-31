#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views.phone.device import index, historical, information_details
from app.views.phone.user import my_information, login, logout, personal,workorder,warning
urlpatterns = [
    url(r'index/$', index, name="phone_index"),
    url(r'historical/$', historical, name="historical"),
    url(r'informationDetails/$', information_details, name="information_details"),
    url(r'myInformation/$', my_information, name="phone/my_information"),
    url(r'personal/$', personal, name="personal"),
    url(r'workorder/$', workorder, name="workorder"),
    url(r'warning/$', warning, name="warning"),
    url(r'user/login/$', login, name="login"),
    url(r'user/logout/$', logout, name="logout"),
    url(r'aboutUs/$', TemplateView.as_view(template_name="phone/aboutUs.html")),
]