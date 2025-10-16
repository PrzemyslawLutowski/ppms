# Fragment kodu ppms\plan_result\tasks.py (celery)
import django

django.setup()

from celery import shared_task
from celery.utils.log import get_task_logger
from . import models
from datetime import datetime, timedelta
import math

logger = get_task_logger(__name__)
@shared_task
def plan_result_schedule_task():
    plan_result_task()
    # plan_result_to_variable_task()


def plan_result_task():
    lines = models.ProductionLines.objects.all()
    time_now = datetime.now().time()

    for line in lines:

        if line.counting_status:

            if line.planned_working_time.start_time < time_now < line.planned_working_time.end_time:
                print("praca")

                hh_ws, mm_ws, ss_ws = map(int, str(line.planned_working_time.start_time).split(":"))
                delta_ws = timedelta(hours=hh_ws, minutes=mm_ws, seconds=ss_ws)

                hh_we, mm_we, ss_we = map(int, str(line.planned_working_time.end_time).split(":"))
                delta_we = timedelta(hours=hh_we, minutes=mm_we, seconds=ss_we)

                hh, mm, ss = map(int, datetime.now().time().isoformat(timespec="seconds").split(":"))
                delta_tn = timedelta(hours=hh, minutes=mm, seconds=ss)

                planned_breaks_time = 0
                past_break_time = 0

                for brake_time in line.planned_break_time.all():

                    if brake_time.start_time < time_now < brake_time.end_time:
                        print("brake")
                        break

                    else:
                        print("not brake")
                        hh_bs, mm_bs, ss_bs = map(int, str(brake_time.start_time).split(":"))
                        delta_bs = timedelta(hours=hh_bs, minutes=mm_bs, seconds=ss_bs)

                        hh_be, mm_be, ss_be = map(int, str(brake_time.end_time).split(":"))
                        delta_be = timedelta(hours=hh_be, minutes=mm_be, seconds=ss_be)

                        break_time = int(delta_be.total_seconds() - delta_bs.total_seconds())

                        planned_breaks_time += break_time

                        if time_now > brake_time.end_time:
                            past_break_time += break_time

                actual_working_time = int(delta_tn.total_seconds() - delta_ws.total_seconds() - past_break_time)
                planned_working_time = int(delta_we.total_seconds() - delta_ws.total_seconds() - planned_breaks_time)


                for plan_result in line.plan_result.all():
                    plan_result_get = models.PlanResultQuantity.objects.get(id=plan_result.id)
                    plan_result_get.planned_working_time = planned_working_time
                    plan_result_get.actual_working_time = actual_working_time

                    try:
                        planned_cycle_time = planned_working_time / plan_result_get.planned_quantity
                        plan_result_get.planned_cycle_time = math.trunc(planned_cycle_time * 10) / 10

                        verification_quantity = actual_working_time  / plan_result_get.planned_cycle_time

                        plan_result_get.quantity_balance = plan_result.quantity - verification_quantity

                        cycle_time_balance = ((planned_working_time - actual_working_time) /
                                              (plan_result.planned_quantity - plan_result.quantity))
                        plan_result_get.cycle_time_balance = math.trunc(cycle_time_balance * 10) / 10

                    except ZeroDivisionError:
                        plan_result_get.planned_cycle_time = 0.0

                    plan_result_get.save()

                if line.production_line == 0:
                    line_name = "A"

                elif line.production_line == 1:
                    line_name = "B"

                elif line.production_line == 2:
                    line_name = "C"

                elif line.production_line == 3:
                    line_name = "D"

                variable_name = f"LineViewStatus{line_name}"
                line_view_status = models.VariablesModel.objects.get(variable_name=variable_name)
                line_view_status.current_variable_value = "1" if line.counting_status == True else "0"
                line_view_status.save()

                variables_name = [f"PlanValue{line_name}", f"PlanTtValue{line_name}",
                                  f"BalanceTtValue{line_name}", f"BalanceValue{line_name}"]

                for plan_result in line.plan_result.all():
                    plan_value_get = models.VariablesModel.objects.get(variable_name=variables_name[0])
                    plan_value_get.current_variable_value = str(plan_result.planned_quantity)
                    plan_value_get.save()

                    plan_tt_value_get = models.VariablesModel.objects.get(variable_name=variables_name[1])
                    plan_tt_value_get.current_variable_value = str(plan_result.planned_cycle_time)
                    plan_tt_value_get.save()

                    balance_tt_value_get = models.VariablesModel.objects.get(variable_name=variables_name[2])
                    balance_tt_value_get.current_variable_value = str(plan_result.cycle_time_balance)
                    balance_tt_value_get.save()

                    balance_value_get = models.VariablesModel.objects.get(variable_name=variables_name[3])
                    balance_value_get.current_variable_value = str(plan_result.quantity_balance)
                    balance_value_get.save()