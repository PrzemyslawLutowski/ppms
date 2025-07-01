from django.db import models
from variables.models import VariablesModel


class PlannedWorkingTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class PlannedBreakTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class PlanResultQuantity(models.Model):
    variable = models.OneToOneField(VariablesModel, on_delete=models.CASCADE, unique=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    planned_quantity = models.PositiveSmallIntegerField(default=0)
    planned_working_time = models.PositiveSmallIntegerField(default=0)
    planned_break_time = models.PositiveSmallIntegerField(default=0)
    planned_cycle_time = models.FloatField(default=0.0)
    actual_working_time = models.PositiveSmallIntegerField(default=0)
    quantity_balance = models.SmallIntegerField(default=0)
    cycle_time_balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'PlanResultQuantity'
        verbose_name_plural = 'PlansResultsQuantity'

    def __str__(self):
        return f"{self.variable}"


class ProductionLines(models.Model):
    LINE = [
        (0, 'Linia-A'),
        (1, 'Linia-B'),
        (2, 'Linia-C'),
        (3, 'Linia-D')
    ]

    SHIFT = [
        (0, 'I-zmiana'),
        (1, 'II-zmiana'),
        (2, 'III-zmiana')
    ]

    production_line = models.PositiveSmallIntegerField(choices=LINE, default=0)
    shift = models.PositiveSmallIntegerField(choices=SHIFT, default=0)
    plan_result = models.ManyToManyField(PlanResultQuantity, blank=True)
    counting_status = models.BooleanField(default=False)
    planned_working_time = models.OneToOneField(PlannedWorkingTime, on_delete=models.CASCADE)
    planned_break_time = models.ManyToManyField(PlannedBreakTime, blank=True)

    class Meta:
        unique_together = ('production_line', 'shift')
        verbose_name = 'ProductionLine'
        verbose_name_plural = 'ProductionLines'

    def __str__(self):
        return f"{self.production_line}"
