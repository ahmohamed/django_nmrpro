# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_nmrpro.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionSpec',
            fields=[
                ('s_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('_original_array', models.BinaryField()),
                ('_original_udic', models.TextField()),
                ('_original_dtype', models.CharField(max_length=15)),
                ('_original_shape', models.CharField(max_length=31)),
                ('_history', models.BinaryField(blank=True)),
                ('accessed', django_nmrpro.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('session', models.ForeignKey(to='sessions.Session')),
            ],
        ),
    ]
