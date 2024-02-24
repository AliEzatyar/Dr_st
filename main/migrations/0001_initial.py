# Generated by Django 4.2.7 on 2024-02-23 01:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bgt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='بدون نام', max_length=25)),
                ('company', models.CharField(default='بدون شرکت', max_length=25)),
                ('bg_price', models.PositiveIntegerField(default=0)),
                ('amount', models.PositiveSmallIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bg_date', models.DateField(default=django.utils.timezone.now)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='drugs')),
                ('bgt_bill', models.PositiveSmallIntegerField(default=0)),
                ('unique', models.CharField(blank=True, max_length=100, unique=True)),
                ('currency', models.CharField(default='AFS', max_length=3)),
                ('sld_amount', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('baqi_amount', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('total', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name', 'bgt_bill', 'bg_date'],
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('name', models.CharField(default='بدون نام', max_length=25)),
                ('company', models.CharField(max_length=25)),
                ('existing_amount', models.PositiveSmallIntegerField(default=0)),
                ('photo', models.ImageField(null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('unique', models.CharField(blank=True, default='no name and company', max_length=60, primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['name', 'company'],
            },
        ),
        migrations.CreateModel(
            name='Sld',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='بدون نام', max_length=30)),
                ('amount', models.PositiveSmallIntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sld_date', models.DateField(default=django.utils.timezone.now)),
                ('company', models.CharField(default='بدون شرکت', max_length=30)),
                ('profite', models.IntegerField(blank=True)),
                ('sld_bill', models.IntegerField(default=0)),
                ('currency', models.CharField(default='AFS', max_length=3)),
                ('unique', models.CharField(blank=True, max_length=100)),
                ('total', models.IntegerField(default=0)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slds', to='main.drug')),
            ],
            options={
                'ordering': ['name', 'sld_date', 'sld_bill'],
            },
        ),
        migrations.AddIndex(
            model_name='drug',
            index=models.Index(fields=['name'], name='main_drug_name_bffea9_idx'),
        ),
        migrations.AddIndex(
            model_name='drug',
            index=models.Index(fields=['company'], name='main_drug_company_f91d44_idx'),
        ),
        migrations.AddField(
            model_name='bgt',
            name='drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bgts', to='main.drug'),
        ),
        migrations.AddIndex(
            model_name='sld',
            index=models.Index(fields=['name'], name='main_sld_name_34b3e6_idx'),
        ),
        migrations.AddIndex(
            model_name='bgt',
            index=models.Index(fields=['name'], name='main_bgt_name_ee65a3_idx'),
        ),
        migrations.AddIndex(
            model_name='bgt',
            index=models.Index(fields=['company'], name='main_bgt_company_32752e_idx'),
        ),
    ]
