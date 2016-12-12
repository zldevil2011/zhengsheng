# coding=utf-8
from app.models import AppUser, Device, Data, Parameter, WorkOrder, Event
from rest_framework import serializers

class AppUserSerializer(serializers.ModelSerializer):
    device = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    class Meta:
        model = AppUser
        fields = (
            'id', 'username', 'telephone', 'email', 'device','address','user_username'
        )

    def get_device(self, obj):
        device = obj.device
        return DeviceSerializer(device).data
    def get_user_username(self, obj):
        return obj.user.username


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'device_id', 'city_code', 'village_code', 'building_code', 'unit_code',
            'room_code', 'manufacture_date', 'gateway_code',
            'meter_box', 'device_status'
        )


class WorkOrderSerializer(serializers.ModelSerializer):
    appuser = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    class Meta:
        model = WorkOrder
        fields = (
            'num', 'type', 'appuser', 'content', 'status', 'time'
        )

    def get_appuser(self, obj):
        appuser = obj.appuser
        return AppUserSerializer(appuser).data

    def get_time(self, obj):
        return obj.time.strftime('%Y-%m-%d %H:%M:%S')


class DataSerializer(serializers.ModelSerializer):
    device_id = serializers.SerializerMethodField()
    tempBT = serializers.SerializerMethodField()
    class Meta:
        model = Data
        fields = (
            'device_id', 'temp', 'tempT', 'powerV', 'powerI', 'powerT', 'tempB', 'tempBT', 'faultB', 'faultBT'
        )

    def get_device_id(self, obj):
        device = obj.device_id
        return DeviceSerializer(device).data

    def get_tempBT(self, obj):
        return obj.tempBT.strftime('%Y-%m-%d %H:%M:%S')


class EventSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = (
            'name_no', 'name', 'time', 'content'
        )
    def get_time(self, obj):
        return obj.time.strftime('%Y-%m-%d %H:%M:%S')