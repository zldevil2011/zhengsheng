#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views import index, user
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="app/welcome.html")),
    url(r'^admin_login/$', index.admin_login, name="admin_login"),
    url(r'^admin_index/$', index.admin_index, name="admin_index"),
    url(r'^admin_account/$', user.admin_account, name="admin_account"),
    url(r'^admin_work_order/$', user.admin_work_order, name="admin_work_order"),
]