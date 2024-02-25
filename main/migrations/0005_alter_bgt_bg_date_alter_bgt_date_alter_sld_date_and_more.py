# Generated by Django 4.2.7 on 2024-02-25 08:59

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_sld_bgt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bgt',
            name='bg_date',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bgt',
            name='date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sld',
            name='date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sld',
            name='sld_date',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]
