# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('productships', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productincrement',
            name='owner',
        ),
        migrations.AddField(
            model_name='productincrement',
            name='tags',
            field=djorm_pgarray.fields.TextArrayField(verbose_name='tags', dbtype='text'),
        ),
        migrations.AddField(
            model_name='productincrement',
            name='version',
            field=models.IntegerField(default=1, verbose_name='version'),
        ),
    ]
