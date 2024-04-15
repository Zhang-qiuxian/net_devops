from rest_framework.routers import SimpleRouter

from apps.device.api.api_device import device, device_snmp_templates, device_company
from apps.cron.api.api_cron import clock_schedule,interval_schedule,periodic_task,cron_solar_schedules,periodic_tasks
from apps.cron.api.api_cron_result import task_result,group_result,chord_counter

router = SimpleRouter()
router.register(prefix="device", viewset=device, basename="device")
router.register(prefix="device-snmp", viewset=device_snmp_templates, basename="device-snmp")
router.register(prefix="device-company", viewset=device_company, basename="device-company")
router.register(prefix="cron-clock", viewset=clock_schedule, basename="cron-clock")
router.register(prefix="cron-interval", viewset=interval_schedule, basename="cron-interval")
router.register(prefix="cron-periodic", viewset=periodic_task, basename="cron-periodic")
router.register(prefix="cron-schedules", viewset=cron_solar_schedules, basename="cron-schedules")
router.register(prefix="cron-periodics", viewset=periodic_tasks, basename="cron-periodics")
router.register(prefix="task_result", viewset=task_result, basename="task_result")
router.register(prefix="group_result", viewset=group_result, basename="group_result")
router.register(prefix="chord_counter", viewset=chord_counter, basename="chord_counter")

api_url = [
    # path('admin/', admin.site.urls),
]
