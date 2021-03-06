from datetime import timedelta
from os import path

from django.conf import settings


ORCHESTRATION_OS_CHOICES = getattr(settings, 'ORCHESTRATION_OS_CHOICES', (
    ('LINUX', "Linux"),
))


ORCHESTRATION_DEFAULT_OS = getattr(settings, 'ORCHESTRATION_DEFAULT_OS', 'LINUX')


ORCHESTRATION_SSH_KEY_PATH = getattr(settings, 'ORCHESTRATION_SSH_KEY_PATH', 
    path.join(path.expanduser('~'), '.ssh/id_rsa'))


ORCHESTRATION_ROUTER = getattr(settings, 'ORCHESTRATION_ROUTER',
    'orchestra.contrib.orchestration.models.Route'
)


ORCHESTRATION_TEMP_SCRIPT_PATH = getattr(settings, 'ORCHESTRATION_TEMP_SCRIPT_PATH',
    '/dev/shm'
)


ORCHESTRATION_DISABLE_EXECUTION = getattr(settings, 'ORCHESTRATION_DISABLE_EXECUTION',
    False
)


ORCHESTRATION_BACKEND_CLEANUP_DELTA = getattr(settings, 'ORCHESTRATION_BACKEND_CLEANUP_DELTA',
    timedelta(days=40)
)
