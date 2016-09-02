from django.contrib import admin
from app.models import Area, Adminer, Data, Device, AppUser, WorkOrder, Repairing, Fund


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'village')


class AdminerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telephone', 'area')


class DataAdmin(admin.ModelAdmin):
    list_display = ('id', 'voltage', 'electricity', 'total_power')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'name', 'status')


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'telephone', 'email')


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'type', 'status')


class RepairingAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'status')


class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'appuser', 'total_num')

admin.site.register(Area, AreaAdmin)
admin.site.register(Adminer, AdminerAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Repairing, RepairingAdmin)
admin.site.register(Fund, FundAdmin)

# Register your models here.
