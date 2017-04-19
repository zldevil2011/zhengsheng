#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.appView import user

urlpatterns = [
    url(r'user/login/$', user.login, name="app_user_login"),
    url(r'user/logout/$', user.logout, name="app_user_logout"),
    url(r'user/updateinfo/$', user.update, name="app_user_update"),
    url(r'index/$', user.index, name="app_index"),
]