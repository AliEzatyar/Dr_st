# Generated by Django 4.2.13 on 2024-06-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_ccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prof',
            options={'verbose_name': 'Profile'},
        ),
        migrations.AddField(
            model_name='prof',
            name='phone',
            field=models.CharField(default='No Number', max_length=12),
        ),
        migrations.AlterField(
            model_name='prof',
            name='photo',
            field=models.ImageField(null=True, upload_to='Owners/'),
        ),
    ]
