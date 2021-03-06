# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import orchestra.core.validators
from django.conf import settings


class Migration(migrations.Migration):

#    dependencies = [
#        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
#    ]

    operations = [
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(validators=[orchestra.core.validators.validate_username], unique=True, help_text='Required. 64 characters or fewer. Letters, digits and ./-/_ only.', max_length=32, verbose_name='username')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('home', models.CharField(max_length=256, help_text='Starting location when login with this no-shell user.', blank=True, verbose_name='home')),
                ('directory', models.CharField(max_length=256, help_text="Optional directory relative to user's home.", blank=True, verbose_name='directory')),
                ('shell', models.CharField(default='/dev/null', choices=[('/dev/null', 'No shell, FTP only'), ('/bin/rssh', 'No shell, SFTP/RSYNC only'), ('/bin/bash', '/bin/bash'), ('/bin/sh', '/bin/sh')], max_length=32, verbose_name='shell')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this account should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
#                ('account', models.ForeignKey(related_name='systemusers', to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('groups', models.ManyToManyField(help_text='A new group will be created for the user. Which additional groups would you like them to be a member of?', blank=True, to='systemusers.SystemUser')),
            ],
        ),
    ]
