# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# 区域
class Area(models.Model):
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    village = models.CharField(max_length=100, null=True)


# adminer的信息
class Adminer(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100, default="000")
    area = models.CharField(max_length=200, default="area")
    time = models.DateTimeField(auto_created=True, null=True)

    def __unicode__(self):
        return self.name


# 节点数据表
class Data(models.Model):
    voltage = models.FloatField(default=0.0)
    electricity = models.FloatField(default=0.0)
    power = models.FloatField(default=0.0)
    total_power = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)      # 节点温度
    instantVoltage = models.FloatField(default=0.0, null=True)   # 瞬时电压
    instantElectricity = models.FloatField(default=0.0, null=True)   # 瞬时电流
    effectiveVoltage = models.FloatField(default=0.0, null=True)    # 有效电压
    effectiveElectricity = models.FloatField(default=0.0, null=True)   # 有效电流
    electricalEnergy = models.FloatField(default=0.0, null=True)   # 电能
    lopsidedVoltage = models.FloatField(default=0.0, null=True)   # 三相电压不平衡
    lopsidedElectricity = models.FloatField(default=0.0, null=True)   # 三相电流不平衡
    # 负序电压 负序电流 功率因数

    def __unicode__(self):
        return str(self.id)


# 设备信息，包括终端，配电箱，网关
class Device(models.Model):
    device_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    status = models.CharField(max_length=200, null=True)
    install_time = models.DateTimeField(auto_created=True)
    type = models.CharField(max_length=100, null=True)
    data = models.ForeignKey(Data, related_name='device')

    def __unicode__(self):
        return self.name


# 用户表，存储用户的相关信息
class AppUser(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=200)
    sex = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    device = models.ForeignKey(Device, related_name='appuser', null=True)
    register_time = models.DateTimeField(auto_created=True)
    money = models.FloatField(default=0.0)
    telephone = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username


# 工单
class WorkOrder(models.Model):
    num = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=100, null=True)
    appuser = models.ForeignKey(AppUser, related_name='workOrder')
    content = models.CharField(max_length=1000, null=True)
    status = models.CharField(max_length=200, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.num


# 维修
class Repairing(models.Model):
    num = models.CharField(max_length=100, null=True)
    device = models.ForeignKey(Device, related_name='repairing')
    status = models.CharField(max_length=100, null=True)
    time = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.num


class Fund(models.Model):
    appuser = models.ForeignKey(AppUser, related_name="fund")
    num = models.FloatField(default=0.0)
    total_num = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=100, default="失败")

    def __unicode__(self):
        return str(self.id)



# Create your models here.
