# Generated by Django 5.0.6 on 2024-06-14 12:08

import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_bgt_options_alter_sld_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.BooleanField(default=False)),
                ('customer', models.CharField(max_length=60)),
                ('date', models.CharField(max_length=60)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='bgt',
            name='date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 6, 14)),
        ),
        migrations.AlterField(
            model_name='sld',
            name='date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 6, 14)),
        ),
    ]