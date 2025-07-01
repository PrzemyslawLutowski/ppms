from django.db import models
from main.models import DateTimeStampedModel


class VariablesModel(DateTimeStampedModel):
    TYPE_VARIABLE = [
        (0, 'boolean'),
        (1, 'integer'),
        (2, 'string'),
        (3, 'float')
    ]

    variable_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    variable_address = models.CharField(max_length=100, blank=False, null=False)
    variable_type = models.PositiveSmallIntegerField(choices=TYPE_VARIABLE, default=0)
    current_variable_value = models.CharField(max_length=100, blank=True, null=True)
    true_value_counter = models.PositiveSmallIntegerField(default=0)
    false_value_counter = models.PositiveSmallIntegerField(default=0)
    true_value_current_time = models.FloatField(default=0.0)
    false_value_current_time = models.FloatField(default=0.0)
    true_value_time = models.FloatField(default=0.0)
    false_value_time = models.FloatField(default=0.0)
    true_value_timer_time = models.FloatField(default=0.0)
    false_value_timer_time = models.FloatField(default=0.0)
    true_value_cycle_time = models.FloatField(default=0.0)
    false_value_cycle_time = models.FloatField(default=0.0)

    class Meta:
        ordering = ('variable_address',)
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    def __str__(self):
        return str(self.variable_name + ' ' + self.variable_address)


class DevicesModel(DateTimeStampedModel):
    PROTOCOL = [
        (0, 'modbus_tcp'),
        (1, 'tcp_ip'),
        (2, 'internal_ppms')
    ]

    TYPE = [
        (0, 'binary'),
        (1, 'ascii')
    ]

    devices_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    devices_ip = models.CharField(max_length=15, blank=True, null=True, default='127.0.0.1')
    connection_protocol = models.PositiveIntegerField(choices=PROTOCOL, default=0)
    communication_type = models.PositiveIntegerField(choices=TYPE, blank=True, null=True)
    communication_port = models.CharField(max_length=4, blank=True, null=True)
    variables = models.ManyToManyField(VariablesModel, blank=True)

    class Meta:
        ordering = ('devices_name',)
        unique_together = ('devices_name', 'devices_ip', 'connection_protocol', 'communication_type', 'communication_port')
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return str(self.devices_name + ' ' + self.devices_ip)




