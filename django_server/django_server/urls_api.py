from django.urls import path, include

from rest_framework.routers import SimpleRouter

from apps.device.api.api_device import device, device_snmp_templates, device_company, device_ip, device_serial, \
    device_system, device_interface, device_arp
from apps.cron.api.api_cron import clock_schedule, interval_schedule, periodic_task, crontab_schedules
from apps.cron.api.api_cron_result import task_result

router = SimpleRouter()
# device
router.register(prefix="device/info", viewset=device, basename="device-info")
router.register(prefix="device/snmp", viewset=device_snmp_templates, basename="device-snmp")
router.register(prefix="device/company", viewset=device_company, basename="device-company")
router.register(prefix="device/ip", viewset=device_ip, basename="device-ip")
router.register(prefix="device/system", viewset=device_system, basename="device-system")
router.register(prefix="device/serial", viewset=device_serial, basename="device-serial")
router.register(prefix="device/interface", viewset=device_interface, basename="device-interface")
router.register(prefix="device/arp", viewset=device_arp, basename="device-arp")

# cron
router.register(prefix="cron/clock", viewset=clock_schedule, basename="cron-clock")
router.register(prefix="cron/interval", viewset=interval_schedule, basename="cron-interval")
router.register(prefix="cron/crontab", viewset=crontab_schedules, basename="cron-crontab")
router.register(prefix="cron/periodic", viewset=periodic_task, basename="cron-periodic")
router.register(prefix="cron/task_result", viewset=task_result, basename="task_result")

api_url = [
    # path('device/', include(router.urls)),
]
