from django.conf import settings

from django.utils.translation import ugettext_lazy as _


SYSTEMUSERS_SHELLS = getattr(settings, 'SYSTEMUSERS_SHELLS', (
    ('/dev/null', _("No shell, FTP only")),
    ('/bin/rssh', _("No shell, SFTP/RSYNC only")),
    ('/bin/bash', "/bin/bash"),
    ('/bin/sh', "/bin/sh"),
))


SYSTEMUSERS_DEFAULT_SHELL = getattr(settings, 'SYSTEMUSERS_DEFAULT_SHELL',
    '/dev/null'
)


SYSTEMUSERS_DISABLED_SHELLS = getattr(settings, 'SYSTEMUSERS_DISABLED_SHELLS', (
    '/dev/null',
    '/bin/rssh',
))


SYSTEMUSERS_HOME = getattr(settings, 'SYSTEMUSERS_HOME',
    '/home/%(user)s'
)


SYSTEMUSERS_FTP_LOG_PATH = getattr(settings, 'SYSTEMUSERS_FTP_LOG_PATH',
    '/var/log/vsftpd.log'
)


SYSTEMUSERS_MAIL_LOG_PATH = getattr(settings, 'SYSTEMUSERS_MAIL_LOG_PATH',
    '/var/log/exim4/mainlog'
)

SYSTEMUSERS_DEFAULT_GROUP_MEMBERS = getattr(settings, 'SYSTEMUSERS_DEFAULT_GROUP_MEMBERS',
    ('www-data',)
)


SYSTEMUSERS_MOVE_ON_DELETE_PATH = getattr(settings, 'SYSTEMUSERS_MOVE_ON_DELETE_PATH',
    ''
)
