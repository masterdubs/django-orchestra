from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SERVICES_SERVICE_TAXES = getattr(settings, 'SERVICES_SERVICE_TAXES', (
    (0, _("Duty free")),
    (21, "21%"),
))


SERVICES_SERVICE_DEFAULT_TAX = getattr(settings, 'SERVICES_SERVICE_DEFAULT_TAX',
    0
)


SERVICES_SERVICE_ANUAL_BILLING_MONTH = getattr(settings, 'SERVICES_SERVICE_ANUAL_BILLING_MONTH',
    1
)


SERVICES_ORDER_MODEL = getattr(settings, 'SERVICES_ORDER_MODEL',
    'orders.Order'
)


SERVICES_RATE_CLASS = getattr(settings, 'SERVICES_RATE_CLASS',
    'orchestra.contrib.plans.models.Rate'
)


SERVICES_DEFAULT_IGNORE_PERIOD = getattr(settings, 'SERVICES_DEFAULT_IGNORE_PERIOD',
    'TEN_DAYS'
)


SERVICES_IGNORE_ACCOUNT_TYPE = getattr(settings, 'SERVICES_IGNORE_ACCOUNT_TYPE', (
    'superuser',
    'STAFF',
    'FRIEND',
))
