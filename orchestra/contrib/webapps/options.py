import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from orchestra.plugins import Plugin
from orchestra.utils.functional import cached
from orchestra.utils.python import import_class

from . import settings


class AppOption(Plugin):
    PHP = 'PHP'
    PROCESS = 'Process'
    FILESYSTEM = 'FileSystem'
    
    help_text = ""
    group = None
    
    @classmethod
    @cached
    def get_plugins(cls):
        plugins = []
        for cls in settings.WEBAPPS_ENABLED_OPTIONS:
            plugins.append(import_class(cls))
        return plugins
    
    @classmethod
    @cached
    def get_option_groups(cls):
        groups = {}
        for opt in cls.get_plugins():
            try:
                groups[opt.group].append(opt)
            except KeyError:
                groups[opt.group] = [opt]
        return groups
    
    def validate(self):
        if self.regex and not re.match(self.regex, self.instance.value):
            raise ValidationError({
                'value': ValidationError(_("'%(value)s' does not match %(regex)s."),
                    params={
                        'value': self.instance.value,
                        'regex': self.regex
                    }),
            })


class PHPAppOption(AppOption):
    deprecated = None
    group = AppOption.PHP
    
    def validate(self):
        super(PHPAppOption, self).validate()
        if self.deprecated:
            php_version = self.instance.webapp.type_instance.get_php_version_number()
            if php_version and self.deprecated and float(php_version) > self.deprecated:
                raise ValidationError(
                    _("This option is deprecated since PHP version %s.") % str(self.deprecated)
                )


class PublicRoot(AppOption):
    name = 'public-root'
    verbose_name = _("Public root")
    help_text = _("Document root relative to webapps/&lt;webapp&gt;/")
    regex = r'[^ ]+'
    group = AppOption.FILESYSTEM


class Timeout(AppOption):
    name = 'timeout'
    # FCGID FcgidIOTimeout
    # FPM pm.request_terminate_timeout
    # PHP max_execution_time ini
    verbose_name = _("Process timeout")
    help_text = _("Maximum time in seconds allowed for a request to complete (a number between 0 and 999).<br>"
                  "Also sets <tt>max_request_time</tt> when php-cgi is used.")
    regex = r'^[0-9]{1,3}$'
    group = AppOption.PROCESS


class Processes(AppOption):
    name = 'processes'
    # FCGID MaxProcesses
    # FPM pm.max_children
    verbose_name = _("Number of processes")
    help_text = _("Maximum number of children that can be alive at the same time (a number between 0 and 9).")
    regex = r'^[0-9]{1,2}$'
    group = AppOption.PROCESS


class PHPEnableFunctions(PHPAppOption):
    name = 'enable_functions'
    verbose_name = _("Enable functions")
    help_text = ','.join(settings.WEBAPPS_PHP_DISABLED_FUNCTIONS)
    regex = r'^[\w\.,-]+$'


class PHPAllowURLInclude(PHPAppOption):
    name = 'allow_url_include'
    verbose_name = _("Allow URL include")
    help_text = _("Allows the use of URL-aware fopen wrappers with include, include_once, require, "
                "require_once (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPAllowURLFopen(PHPAppOption):
    name = 'allow_url_fopen'
    verbose_name = _("Allow URL fopen")
    help_text = _("Enables the URL-aware fopen wrappers that enable accessing URL object like files (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPAutoAppendFile(PHPAppOption):
    name = 'auto_append_file'
    verbose_name = _("Auto append file")
    help_text = _("Specifies the name of a file that is automatically parsed after the main file.")
    regex = r'^[\w\.,-/]+$'


class PHPAutoPrependFile(PHPAppOption):
    name = 'auto_prepend_file'
    verbose_name = _("Auto prepend file")
    help_text = _("Specifies the name of a file that is automatically parsed before the main file.")
    regex = r'^[\w\.,-/]+$'


class PHPDateTimeZone(PHPAppOption):
    name = 'date.timezone'
    verbose_name = _("date.timezone")
    help_text = _("Sets the default timezone used by all date/time functions (Timezone string 'Europe/London').")
    regex = r'^\w+/\w+$'


class PHPDefaultSocketTimeout(PHPAppOption):
    name = 'default_socket_timeout'
    verbose_name = _("Default socket timeout")
    help_text = _("Number between 0 and 999.")
    regex = r'^[0-9]{1,3}$'


class PHPDisplayErrors(PHPAppOption):
    name = 'display_errors'
    verbose_name = _("Display errors")
    help_text = _("Determines whether errors should be printed to the screen as part of the output or "
                  "if they should be hidden from the user (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPExtension(PHPAppOption):
    name = 'extension'
    verbose_name = _("Extension")
    regex = r'^[^ ]+$'


class PHPMagicQuotesGPC(PHPAppOption):
    name = 'magic_quotes_gpc'
    verbose_name = _("Magic quotes GPC")
    help_text = _("Sets the magic_quotes state for GPC (Get/Post/Cookie) operations (On or Off) "
                  "<b>DEPRECATED as of PHP 5.3.0</b>.")
    regex = r'^(On|Off|on|off)$'
    deprecated = 5.3


class PHPMagicQuotesRuntime(PHPAppOption):
    name = 'magic_quotes_runtime'
    verbose_name = _("Magic quotes runtime")
    help_text = _("Functions that return data from any sort of external source will have quotes escaped "
                  "with a backslash (On or Off) <b>DEPRECATED as of PHP 5.3.0</b>.")
    regex = r'^(On|Off|on|off)$'
    deprecated = 5.3


class PHPMaginQuotesSybase(PHPAppOption):
    name = 'magic_quotes_sybase'
    verbose_name = _("Magic quotes sybase")
    help_text = _("Single-quote is escaped with a single-quote instead of a backslash (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPMaxInputTime(PHPAppOption):
    name = 'max_input_time'
    verbose_name = _("Max input time")
    help_text = _("Maximum time in seconds a script is allowed to parse input data, like POST and GET "
                "(Integer between 0 and 999).")
    regex = r'^[0-9]{1,3}$'


class PHPMaxInputVars(PHPAppOption):
    name = 'max_input_vars'
    verbose_name = _("Max input vars")
    help_text = _("How many input variables may be accepted (limit is applied to $_GET, $_POST "
                "and $_COOKIE superglobal separately) (Integer between 0 and 9999).")
    regex = r'^[0-9]{1,4}$'


class PHPMemoryLimit(PHPAppOption):
    name = 'memory_limit'
    verbose_name = _("Memory limit")
    help_text = _("This sets the maximum amount of memory in bytes that a script is allowed to allocate "
                  "(Value between 0M and 999M).")
    regex = r'^[0-9]{1,3}M$'


class PHPMySQLConnectTimeout(PHPAppOption):
    name = 'mysql.connect_timeout'
    verbose_name = _("Mysql connect timeout")
    help_text = _("Number between 0 and 999.")
    regex = r'^([0-9]){1,3}$'


class PHPOutputBuffering(PHPAppOption):
    name = 'output_buffering'
    verbose_name = _("Output buffering")
    help_text = _("Turn on output buffering (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPRegisterGlobals(PHPAppOption):
    name = 'register_globals'
    verbose_name = _("Register globals")
    help_text = _("Whether or not to register the EGPCS (Environment, GET, POST, Cookie, Server) "
                  "variables as global variables (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPPostMaxSize(PHPAppOption):
    name = 'post_max_size'
    verbose_name = _("Post max size")
    help_text = _("Sets max size of post data allowed (Value between 0M and 999M).")
    regex = r'^[0-9]{1,3}M$'


class PHPSendmailPath(PHPAppOption):
    name = 'sendmail_path'
    verbose_name = _("Sendmail path")
    help_text = _("Where the sendmail program can be found.")
    regex = r'^[^ ]+$'


class PHPSessionBugCompatWarn(PHPAppOption):
    name = 'session.bug_compat_warn'
    verbose_name = _("Session bug compat warning")
    help_text = _("Enables an PHP bug on session initialization for legacy behaviour (On or Off).")
    regex = r'^(On|Off|on|off)$'


class PHPSessionAutoStart(PHPAppOption):
    name = 'session.auto_start'
    verbose_name = _("Session auto start")
    help_text = _("Specifies whether the session module starts a session automatically on request "
                "startup (On or Off).")
    regex = r'^(On|Off|on|off)$'
    group = AppOption.PHP


class PHPSafeMode(PHPAppOption):
    name = 'safe_mode'
    verbose_name = _("Safe mode")
    help_text = _("Whether to enable PHP's safe mode (On or Off) <b>DEPRECATED as of PHP 5.3.0</b>")
    regex = r'^(On|Off|on|off)$'
    deprecated=5.3


class PHPSuhosinPostMaxVars(PHPAppOption):
    name = 'suhosin.post.max_vars'
    verbose_name = _("Suhosin POST max vars")
    help_text = _("Number between 0 and 9999.")
    regex = r'^[0-9]{1,4}$'


class PHPSuhosinGetMaxVars(PHPAppOption):
    name = 'suhosin.get.max_vars'
    verbose_name = _("Suhosin GET max vars")
    help_text = _("Number between 0 and 9999.")
    regex = r'^[0-9]{1,4}$'


class PHPSuhosinRequestMaxVars(PHPAppOption):
    name = 'suhosin.request.max_vars'
    verbose_name = _("Suhosin request max vars")
    help_text = _("Number between 0 and 9999.")
    regex = r'^[0-9]{1,4}$'


class PHPSuhosinSessionEncrypt(PHPAppOption):
    name = 'suhosin.session.encrypt'
    verbose_name = _("Suhosin session encrypt")
    help_text = _("On or Off")
    regex = r'^(On|Off|on|off)$'


class PHPSuhosinSimulation(PHPAppOption):
    name = 'suhosin.simulation'
    verbose_name = _("Suhosin simulation")
    help_text = _("On or Off")
    regex = r'^(On|Off|on|off)$'


class PHPSuhosinExecutorIncludeWhitelist(PHPAppOption):
    name = 'suhosin.executor.include.whitelist'
    verbose_name = _("Suhosin executor include whitelist")
    regex = r'.*$'


class PHPUploadMaxFileSize(PHPAppOption):
    name = 'upload_max_filesize'
    verbose_name = _("Upload max filezise")
    help_text = _("Value between 0M and 999M.")
    regex = r'^[0-9]{1,3}M$'


class PHPZendExtension(PHPAppOption):
    name = 'zend_extension'
    verbose_name = _("Zend extension")
    regex = r'^[^ ]+$'
