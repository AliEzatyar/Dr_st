# Generated by Django 5.0.6 on 2024-06-14 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_sld_bill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sld',
            old_name='bill',
            new_name='bill_object',
        ),
    ]
