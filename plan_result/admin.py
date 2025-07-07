from django.contrib import admin
from . import models


@admin.register(models.ProductionLines)
class ProductionLinesAdmin(admin.ModelAdmin):
    list_display = [
        'production_line',
        'shift'
    ]


@admin.register(models.PlannedWorkingTime)
class PlannedWorkingTimeAdmin(admin.ModelAdmin):
    list_display = [
        'start_time',
        'end_time'
    ]


@admin.register(models.PlannedBreakTime)
class PlannedBreakTimeAdmin(admin.ModelAdmin):
    list_display = [
        'production_line',
        'start_time',
        'end_time'
    ]


@admin.register(models.PlanResultQuantity)
class PlanResultQuantityAdmin(admin.ModelAdmin):
    list_display = [
        'variable',
        'quantity',
        'planned_quantity',
        'planned_working_time',
        'planned_break_time',
        'planned_cycle_time',
        'actual_working_time',
        'quantity_balance',
        'cycle_time_balance'
    ]
