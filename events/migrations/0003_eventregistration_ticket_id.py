# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-05 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventregistration_has_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='ticket_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unik id som ingen kan gjette seg til..', null=True, verbose_name='unik billett id'),
        ),
    ]