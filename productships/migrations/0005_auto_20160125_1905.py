# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0002_remove_milestone_watchers'),
        ('productships', '0004_productincrement_external_reference'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productincrement',
            options={'verbose_name_plural': 'product_increments', 'verbose_name': 'product_increment', 'ordering': ['project', 'created_date', '-id'], 'permissions': (('view_product_increment', 'Can view product increment'),)},
        ),
        migrations.AddField(
            model_name='productincrement',
            name='milestone',
            field=models.ForeignKey(default=None, verbose_name='milestone', related_name='product_increments', null=True, to='milestones.Milestone', blank=True),
        ),
    ]
