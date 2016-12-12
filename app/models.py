# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# adminer的信息
class Adminer(models.Model):
    name = models.CharField(max_length=32)
    telephone = models.CharField(max_length=20, default="000")
    area = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=200, null=True)
    time = models.DateTimeField(null=True)
    level = models.SmallIntegerField(default=0)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.name


# 设备信息
class Device(models.Model):
    device_id = models.IntegerField(default=0)  # 设备ID
    city_code = models.SmallIntegerField(null=True)  # 省市代码
    village_code = models.SmallIntegerField(null=True)  # 小区代码
    building_code = models.SmallIntegerField(null=True)  # 楼栋编码
    unit_code = models.SmallIntegerField(null=True)  # 单元编码
    room_code = models.SmallIntegerField(null=True)  # 房间编码
    manufacture_date = models.DateTimeField(null=True)  # 生产日期
    gateway_code = models.SmallIntegerField(null=True)  # 网关编号，区域内编号
    meter_box = models.SmallIntegerField(null=True)  # 表箱编号
    device_status = models.CharField(max_length=32, default='未安装')  # 设备状态 是否投入使用

    def __unicode__(self):
        return str(self.device_id)


# 用户表，存储用户的相关信息
class AppUser(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=16)
    address = models.CharField(max_length=128)
    register_time = models.DateTimeField(null=True)
    telephone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=32, null=True)
    money = models.FloatField(default=0.0)
    password = models.CharField(max_length=32, null=True)
    device = models.ForeignKey(Device, related_name="appuser", null=True)

    def __unicode__(self):
        return self.username


# 节点数据表
class Data(models.Model):
    device_id = models.ForeignKey(Device, related_name='device', null=True)
    temp = models.FloatField(null=True)     # 用户电缆温度
    tempT = models.DateTimeField(null=True)     # 用户电缆温度采集时间
    powerV = models.FloatField(null=True)       # 有功电能
    powerI = models.FloatField(null=True)       # 无功电能
    powerT = models.DateTimeField(null=True)        # 电能采集时间
    tempB = models.SmallIntegerField(null=True)     # 高温报警标示1，0
    tempBT = models.DateTimeField(null=True)        # 高温报警时间
    faultB = models.SmallIntegerField(null=True)        # 通信故障报警标示 1，0
    faultBT = models.DateTimeField(null=True)       # 通信故障报警时间
    voltage = models.FloatField(null=True)          # 电压有效值
    electric_current = models.FloatField(null=True)  # 电流有效值
    power_factor = models.FloatField(null=True)     # 功率因数
    active_power = models.FloatField(null=True)     # 有功功率
    reactive_power = models.FloatField(null=True)   # 无功功率
    date_time = models.DateTimeField(null=True)         # 新增数据采集时间

    def __unicode__(self):
        return str(self.id)


# 中继数据，涉及到3相数据
class Relay(models.Model):
    device_id = models.ForeignKey(Device, related_name='relay', null=True)
    a_voltage = models.FloatField(null=True)    # A相电压有效值
    b_voltage = models.FloatField(null=True)    # B相电压有效值
    c_voltage = models.FloatField(null=True)    # C相电压有效值
    a_electric_current = models.FloatField(null=True)   # A相电流有效值
    b_electric_current = models.FloatField(null=True)   # B相电流有效值
    c_electric_current = models.FloatField(null=True)   # C相电流有效值
    a_power_factor = models.FloatField(null=True)     # A相功率因数
    b_power_factor = models.FloatField(null=True)     # B相功率因数
    c_power_factor = models.FloatField(null=True)     # C相功率因数
    a_active_power = models.FloatField(null=True)     # A相有功功率
    b_active_power = models.FloatField(null=True)     # B相有功功率
    c_active_power = models.FloatField(null=True)     # C相有功功率
    a_reactive_power = models.FloatField(null=True)   # A相无功功率
    b_reactive_power = models.FloatField(null=True)   # B相无功功率
    c_reactive_power = models.FloatField(null=True)   # C相无功功率
    a_powerV = models.FloatField(null=True)           # A相有功电能
    b_powerV = models.FloatField(null=True)           # B相有功电能
    c_powerV = models.FloatField(null=True)           # C相有功电能
    t_powerV = models.FloatField(null=True)           # 总有功电能
    a_powerI = models.FloatField(null=True)           # A相无功电能
    b_powerI = models.FloatField(null=True)           # B相无功电能
    c_powerI = models.FloatField(null=True)           # C相无功电能
    t_powerI = models.FloatField(null=True)           # 总无功电能
    data_time = models.DateTimeField(null=True)       # 数据采集时间

    def __unicode__(self):
        return str(self.id)


# 参数表，存储每个网关的设定参数
class Parameter(models.Model):
    device = models.ForeignKey(Device, related_name='parameter', null=True)     # 设备ID
    temperature_t_length = models.SmallIntegerField(null=True)      # 温度采集间隔
    temperature = models.FloatField(null=True)      # 温度阈值设定
    power_get_point1 = models.TimeField(null=True)      # 电能采集点1
    power_get_point2 = models.TimeField(null=True)      # 电能采集点2
    version = models.SmallIntegerField(null=True)       # 版本号

    def __unicode__(self):
        return str(self.version)


# 城市编码
class City(models.Model):
    city_code = models.IntegerField(null=True)     # 城市代码
    city_name = models.CharField(max_length=32, null=True)     # 城市名称

    def __unicode__(self):
        return str(self.city_code)


# 小区编码
class Village(models.Model):
    city = models.ForeignKey(City, related_name = 'village')        # 所属城市外键
    village_code = models.SmallIntegerField(null=True)      # 小区编码
    village_name = models.CharField(max_length=32,null=True)      # 小区名称

    def __unicode__(self):
        return str(self.village_code)


# 工单
class WorkOrder(models.Model):
    num = models.CharField(max_length=36, null=True)
    type = models.CharField(max_length=32, null=True)
    appuser = models.ForeignKey(AppUser, related_name='workOrder')
    content = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=32, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.num


# 维修
class Repairing(models.Model):
    num = models.CharField(max_length=36, null=True)
    device = models.ForeignKey(Device, related_name='repairing')
    status = models.CharField(max_length=32, null=True)
    time = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.num


# 费用管理
class Fund(models.Model):
    appuser = models.ForeignKey(AppUser, related_name="fund")
    num = models.FloatField(default=0.0)
    total_num = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=32, default="缴费失败")

    def __unicode__(self):
        return str(self.id)


# 事件管理
class Event(models.Model):
    name_no = models.IntegerField(default=0)
    device = models.ForeignKey(Device, related_name='event', null=True)
    name = models.CharField(max_length=32, default=0)
    time = models.DateTimeField(null=True)
    content = models.CharField(max_length=32, null=True)

    def __unicode__(self):
        return str(self.pk)


class Feedback(models.Model):
    email = models.CharField(max_length=50, null=True)
    content = models.TextField(default='')
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.pk)
# Create your models here.
