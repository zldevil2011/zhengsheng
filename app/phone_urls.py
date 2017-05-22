#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'index/$', TemplateView.as_view(template_name="phone/index.html")),
    url(r'historical/$', TemplateView.as_view(template_name="phone/historicalData.html")),
    url(r'informationDetails/$', TemplateView.as_view(template_name="phone/informationDetails.html")),
    url(r'myInformation/$', TemplateView.as_view(template_name="phone/myInformation.html")),
]