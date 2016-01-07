# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0027_auto_20150916_1302'),
        ('attachments', '0005_attachment_sha1'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaMarker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_date', models.DateTimeField(verbose_name='created date', default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(verbose_name='modified date')),
                ('marker_content', models.TextField(verbose_name='marker_content', blank=True)),
                ('attachment', models.ForeignKey(to='attachments.Attachment', verbose_name='Product Increment', related_name='markers')),
                ('owner', models.ForeignKey(blank=True, null=True, verbose_name='owner', to=settings.AUTH_USER_MODEL, related_name='change_media_markers')),
            ],
            options={
                'verbose_name': 'media_marker',
                'ordering': ['created_date', 'id'],
                'verbose_name_plural': 'media_markers',
                'permissions': (('view_media_marker', 'Can view media marker'),),
            },
        ),
        migrations.CreateModel(
            name='ProductIncrement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_date', models.DateTimeField(verbose_name='created date', default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(verbose_name='modified date')),
                ('name', models.CharField(blank=True, default='', max_length=500)),
                ('reviewed', models.BooleanField(verbose_name='reviewed', default=False)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('owner', models.ForeignKey(blank=True, null=True, verbose_name='owner', to=settings.AUTH_USER_MODEL, related_name='change_product_increments')),
                ('project', models.ForeignKey(to='projects.Project', verbose_name='project', related_name='product_increments')),
            ],
        ),
    ]
