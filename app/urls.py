#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import index
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="app/welcome.html")),
    url(r'^admin_login/$', index.admin_login, name="admin_login"),
    url(r'^admin_index/$', index.admin_index, name="admin_index"),
]