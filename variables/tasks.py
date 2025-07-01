import django

django.setup()

from celery import shared_task
from celery.utils.log import get_task_logger
from .models import VariablesModel, DevicesModel
from datetime import datetime, timezone, time
from django.conf import settings
from timeit import default_timer as timer
from pymodbus.client import ModbusTcpClient
import socket
import time
import json
import os


logger = get_task_logger(__name__)
@shared_task()
def variables_schedule_task():
    modbus_read_variables_task()
    # tcp_ip_read_variables_task()


def tcp_ip_read_variables_task():

    devices = DevicesModel.objects.filter(connection_protocol=1)

    for device in devices:
        variables = VariablesModel.objects.filter(devicesmodel=device)
        device = DevicesModel.objects.filter(id=device.id)
        host = device[0].devices_ip
        port = int(device[0].communication_port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            for variable in variables:
                address = str(variable.variable_address)
                s.sendall(address.encode('utf-8'))
                data = s.recv(1024)
                received_data = data.decode('utf-8')
                print(received_data)

                if len(received_data) > 10:

                    if variable.current_variable_value == "0" and received_data[10] == "1":
                        variable_get = VariablesModel.objects.get(id=variable.id)
                        variable_get.variable_value = "1"
                        variable_get.cycle_time_for_true = timer() - variable_get.timer_time_for_true
                        variable_get.value_time_for_false = timer() - variable_get.timer_time_for_false
                        variable_get.timer_time_for_true = timer()
                        print("T", variable_get.cycle_time_for_true)
                        variable_get.save()
                        print(received_data)

                    elif variable.current_variable_value == "1" and received_data[10] == "0":
                        variable_get = VariablesModel.objects.get(id=variable.id)
                        variable_get.variable_value = "0"
                        variable_get.cycle_time_for_false = timer() - variable_get.timer_time_for_false
                        variable_get.value_time_for_true = timer() - variable_get.value_time_for_true
                        variable_get.timer_time_for_false = timer()
                        print("F", variable_get.cycle_time_for_false)
                        variable_get.save()
                        print(received_data)

            s.close()

def modbus_read_variables_task():

    try:

        devices = DevicesModel.objects.filter(connection_protocol=0)

        for device in devices:
            variables = VariablesModel.objects.filter(devicesmodel=device)
            device = DevicesModel.objects.filter(id=device.id)

            host = device[0].devices_ip
            port = int(device[0].communication_port)

            client_1 = ModbusTcpClient(host=host, port=port)
            client_1.connect()

            for variable in variables:
                address = int(variable.variable_address)
                received_data = client_1.read_coils(address=address, count=1).bits[0]
                variable_get = VariablesModel.objects.get(id=variable.id)

                if variable.current_variable_value == "0" and received_data == True:
                    variable_get.current_variable_value = "1"
                    variable_get.true_value_cycle_time = timer() - variable_get.true_value_timer_time
                    variable_get.false_value_time = timer() - variable_get.false_value_timer_time
                    variable_get.true_value_timer_time = timer()
                    variable_get.true_value_counter += 1
                    print("T", variable_get.true_value_cycle_time)
                    print(received_data)

                elif variable.current_variable_value == "1" and received_data == False:
                    variable_get.current_variable_value = "0"
                    variable_get.false_value_cycle_time = timer() - variable_get.false_value_timer_time
                    variable_get.true_value_time = timer() - variable_get.true_value_timer_time
                    variable_get.false_value_timer_time = timer()
                    variable_get.false_value_counter += 1
                    print("F", variable_get.false_value_cycle_time)
                    print(received_data)

                elif variable.current_variable_value == "1" and received_data == True:
                    variable_get.current_value_time_for_true = timer() - variable_get.true_value_counter

                elif variable.current_variable_value == "0" and received_data == False:
                    variable_get.current_value_time_for_false = timer() - variable_get.false_value_timer_time

                variable_get.save()

            client_1.close()

    except:

        pass