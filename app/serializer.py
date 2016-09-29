# coding=utf-8
from app.models import AppUser, Device, Data, Parameter
from rest_framework import serializers

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = (
            'id', 'username', 'telephone', 'email'
        )


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'device_id', 'city_code', 'village_code', 'building_code', 'unit_code',
            'room_code', 'manufacture_date', 'gateway_code',
            'meter_box', 'device_status'
        )