# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# 用户表，存储用户的相关信息
class AppUser(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=200)
    sex = models.IntegerField(default=0)
    home_phone = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=100)
    register_date = models.DateField(auto_now_add=True)


# 节点数据表
class Node(models.Model):
    temperature = models.FloatField(default=0.0)      # 节点温度
    instantVoltage = models.FloatField(default=0.0, null=True)   # 瞬时电压
    instantElectricity = models.FloatField(default=0.0, null=True)   # 瞬时电流
    effectiveVoltage = models.FloatField(default=0.0, null=True)    # 有效电压
    effectiveElectricity = models.FloatField(default=0.0, null=True)   # 有效电流
    electricalEnergy = models.FloatField(default=0.0, null=True)   # 电能
    lopsidedVoltage = models.FloatField(default=0.0, null=True)   # 三相电压不平衡
    lopsidedElectricity = models.FloatField(default=0.0, null=True)   # 三相电流不平衡
    # 负序电压 负序电流 功率因数


# 工单
class WorkOrder(models.Model):
    order_num = models.CharField(max_length=200, null=True)
    order_content = models.CharField(max_length=200, null=True)
    order_type = models.CharField(max_length=200, null=True)
    order_classification = models.CharField(max_length=200, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=200, null=True)
    order_user = models.ForeignKey(AppUser, related_name='appuser')

# Create your models here.
