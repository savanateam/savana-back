# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productships', '0002_auto_20160124_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincrement',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='owner', related_name='change_product_increments', blank=True),
        ),
        migrations.AddField(
            model_name='productincrement',
            name='ref',
            field=models.BigIntegerField(verbose_name='ref', default=None, blank=True, db_index=True, null=True),
        ),
    ]
