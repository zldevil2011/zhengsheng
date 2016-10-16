# coding=utf-8
from app.models import AppUser, Device, Data, Parameter, WorkOrder
from rest_framework import serializers

class AppUserSerializer(serializers.ModelSerializer):
    device = serializers.SerializerMethodField()
    class Meta:
        model = AppUser
        fields = (
            'id', 'username', 'telephone', 'email', 'device'
        )

    def get_device(self, obj):
        device = obj.device
        return DeviceSerializer(device).data


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