from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from orchestra import plugins
from orchestra.plugins.forms import PluginDataForm
from orchestra.utils.functional import cached
from orchestra.utils.python import import_class

from .. import settings
from ..options import AppOption


class AppType(plugins.Plugin):
    name = None
    verbose_name = ""
    help_text= ""
    form = PluginDataForm
    icon = 'orchestra/icons/apps.png'
    unique_name = False
    option_groups = (AppOption.FILESYSTEM, AppOption.PROCESS, AppOption.PHP)
    plugin_field = 'type'
    # TODO generic name like 'execution' ?
    
    @classmethod
    @cached
    def get_plugins(cls):
        plugins = []
        for cls in settings.WEBAPPS_TYPES:
            plugins.append(import_class(cls))
        return plugins
    
    def validate(self):
        """ Unique name validation """
        if self.unique_name:
            if not self.instance.pk and type(self.instance).objects.filter(name=self.instance.name, type=self.instance.type).exists():
                raise ValidationError({
                    'name': _("A WordPress blog with this name already exists."),
                })
    
    @classmethod
    @cached
    def get_options(cls):
        """ Get enabled options based on cls.option_groups """
        groups = AppOption.get_option_groups()
        options = []
        for group in cls.option_groups:
            group_options = groups[group]
            if group is None:
                options.insert(0, (group, group_options))
            else:
                options.append((group, group_options))
        return options
    
    @classmethod
    def get_options_choices(cls):
        """ Generates grouped choices ready to use in Field.choices """
        # generators can not be @cached
        yield (None, '-------')
        for group, options in cls.get_options():
            if group is None:
                for option in options:
                    yield (option.name, option.verbose_name)
            else:
                yield (group, [(op.name, op.verbose_name) for op in options])
    
    def get_detail(self):
        return ''
    
    def save(self):
        pass
    
    def delete(self):
        pass
    
    def get_directive_context(self):
        return {
            'app_id': self.instance.id,
            'app_name': self.instance.name,
            'user': self.instance.account.username,
            'home': self.instance.account.main_systemuser.get_home(),
        }

