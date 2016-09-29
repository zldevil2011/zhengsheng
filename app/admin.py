from django.contrib import admin
from app.models import City, Village, Parameter, Adminer, Data, Device, AppUser, WorkOrder, Repairing, Fund

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_code', 'city_name')


class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'village_code', 'village_name')


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'version')


class AdminerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telephone', 'area')


class DataAdmin(admin.ModelAdmin):
    list_display = ('id', 'temp', 'tempB', 'faultB')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'device_status')


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'telephone', 'email')


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'type', 'status')


class RepairingAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'status')


class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'appuser', 'total_num')

admin.site.register(City, CityAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Adminer, AdminerAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Repairing, RepairingAdmin)
admin.site.register(Fund, FundAdmin)

# Register your models here.
