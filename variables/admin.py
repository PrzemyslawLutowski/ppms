from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.DevicesModel)
class DevicesModelAdmin(admin.ModelAdmin):
    list_display = ['devices_name',
                    'devices_ip',
                    'connection_protocol',
                    'communication_type',
                    'communication_port']


@admin.register(models.VariablesModel)
class VariablesModelAdmin(admin.ModelAdmin):
    list_display = ['variable_name',
                    'variable_address',
                    'variable_type',
                    'current_variable_value',
                    'true_value_counter',
                    'false_value_counter',
                    'true_value_current_time',
                    'false_value_current_time',
                    'true_value_time',
                    'false_value_time',
                    'true_value_timer_time',
                    'false_value_timer_time']

