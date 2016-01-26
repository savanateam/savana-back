# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('productships', '0003_auto_20160124_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincrement',
            name='external_reference',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text', verbose_name='external reference'),
        ),
    ]
