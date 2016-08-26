from django.contrib import admin
from app.models import AppUser, Node, Device, District, WorkOrder, Adminer


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'email')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'location')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'level0', 'level0', 'level0')

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'type', 'classification')

class AdminerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Adminer, AdminerAdmin)
# Register your models here.
