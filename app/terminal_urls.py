#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.terminalView import index
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="terminalUser/base.html")),
    url(r'index/$', index.index, name="terminal-index"),
]