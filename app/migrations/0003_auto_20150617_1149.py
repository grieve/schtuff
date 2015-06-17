# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150617_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(related_name='items', to='app.Category'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='items',
            field=models.ManyToManyField(related_name='checkouts', to='app.Item'),
        ),
    ]
