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

    def __unicode__(self):
        return self.username


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


# 设备信息，对应一个节点node
class Device(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(AppUser, related_name='device_appuser')
    time = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey(Node, related_name='device_node')
    temperature = models.CharField(max_length=200, null=True)


class District(models.Model):
    level0 = models.CharField(max_length=200, null=True)
    level1 = models.CharField(max_length=200, null=True)
    level2 = models.CharField(max_length=200, null=True)


# 工单
class WorkOrder(models.Model):
    num = models.CharField(max_length=200, null=True)
    content = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    classification = models.CharField(max_length=200, null=True)
    workOrderTime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(AppUser, related_name='appuser')


# adminer的信息
class Adminer(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    register_time = models.DateTimeField(auto_now_add = True)
# Create your models here.
