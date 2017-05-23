#coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from app.views.phone.device import index, historical
urlpatterns = [
    url(r'index/$', index, name="phone_index"),
    url(r'historical/$', historical, name="historical"),
    # url(r'historical/$', TemplateView.as_view(template_name="phone/historicalData.html")),
    url(r'informationDetails/$', TemplateView.as_view(template_name="phone/informationDetails.html")),
    url(r'myInformation/$', TemplateView.as_view(template_name="phone/myInformation.html")),
]