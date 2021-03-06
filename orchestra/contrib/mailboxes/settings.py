import os
import textwrap

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from orchestra.settings import ORCHESTRA_BASE_DOMAIN


MAILBOXES_DOMAIN_MODEL = getattr(settings, 'MAILBOXES_DOMAIN_MODEL',
    'domains.Domain'
)


MAILBOXES_HOME = getattr(settings, 'MAILBOXES_HOME',
    '/home/%(name)s/'
)


MAILBOXES_SIEVE_PATH = getattr(settings, 'MAILBOXES_SIEVE_PATH',
    os.path.join(MAILBOXES_HOME, 'Maildir/sieve/orchestra.sieve')
)


MAILBOXES_SIEVETEST_PATH = getattr(settings, 'MAILBOXES_SIEVETEST_PATH',
    '/dev/shm'
)


MAILBOXES_SIEVETEST_BIN_PATH = getattr(settings, 'MAILBOXES_SIEVETEST_BIN_PATH',
    '%(orchestra_root)s/bin/sieve-test'
)


MAILBOXES_VIRTUAL_MAILBOX_MAPS_PATH = getattr(settings, 'MAILBOXES_VIRTUAL_MAILBOX_MAPS_PATH',
    '/etc/postfix/virtual_mailboxes'
)


MAILBOXES_VIRTUAL_ALIAS_MAPS_PATH = getattr(settings, 'MAILBOXES_VIRTUAL_ALIAS_MAPS_PATH',
    '/etc/postfix/virtual_aliases'
)


MAILBOXES_VIRTUAL_ALIAS_DOMAINS_PATH = getattr(settings, 'MAILBOXES_VIRTUAL_ALIAS_DOMAINS_PATH',
    '/etc/postfix/virtual_domains'
)


MAILBOXES_LOCAL_DOMAIN = getattr(settings, 'MAILBOXES_LOCAL_DOMAIN', 
    ORCHESTRA_BASE_DOMAIN
)


MAILBOXES_PASSWD_PATH = getattr(settings, 'MAILBOXES_PASSWD_PATH',
    '/etc/dovecot/passwd'
)


MAILBOXES_MAILBOX_FILTERINGS = getattr(settings, 'MAILBOXES_MAILBOX_FILTERINGS', {
    # value: (verbose_name, filter)
    'DISABLE': (_("Disable"), ''),
    'REJECT': (_("Reject spam"), textwrap.dedent("""
         require ["fileinto","regex","envelope","vacation","reject","relational","comparator-i;ascii-numeric"];
         if header :value "ge" :comparator "i;ascii-numeric" "X-Spam-Score" "5" {
            discard;
            stop;
        }""")),
    'REDIRECT': (_("Archive spam"), textwrap.dedent("""
        require ["fileinto","regex","envelope","vacation","reject","relational","comparator-i;ascii-numeric"];
        if header :value "ge" :comparator "i;ascii-numeric" "X-Spam-Score" "5" {
            fileinto "Spam";
            stop;
        }""")),
    'CUSTOM': (_("Custom filtering"), lambda mailbox: mailbox.custom_filtering),
})


MAILBOXES_MAILBOX_DEFAULT_FILTERING = getattr(settings, 'MAILBOXES_MAILBOX_DEFAULT_FILTERING',
    'REDIRECT'
)


MAILBOXES_MAILDIRSIZE_PATH = getattr(settings, 'MAILBOXES_MAILDIRSIZE_PATH',
    '%(home)s/Maildir/maildirsize'
)


MAILBOXES_LOCAL_ADDRESS_DOMAIN = getattr(settings, 'MAILBOXES_LOCAL_ADDRESS_DOMAIN',
    ORCHESTRA_BASE_DOMAIN
)


MAILBOXES_MAIL_LOG_PATH = getattr(settings, 'MAILBOXES_MAIL_LOG_PATH',
    '/var/log/mail.log'
)


MAILBOXES_MOVE_ON_DELETE_PATH = getattr(settings, 'MAILBOXES_MOVE_ON_DELETE_PATH',
    ''
)
