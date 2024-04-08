from rest_framework.routers import SimpleRouter

from apps.device.api.api_device import device, device_snmp_templates, device_company

router = SimpleRouter()
router.register(prefix="device", viewset=device, basename="device")
router.register(prefix="device-snmp", viewset=device_snmp_templates, basename="device-snmp")
router.register(prefix="device-company", viewset=device_company, basename="device-company")

api_url = [
    # path('admin/', admin.site.urls),
]
