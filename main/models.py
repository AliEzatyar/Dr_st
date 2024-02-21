from django.db import models
from datetime import date

# Create your models here.
from django.utils import timezone


class Drug(models.Model):
    name = models.CharField(max_length=25, unique=True, primary_key=True)
    company = models.CharField(max_length=25)
    existing_amount = models.PositiveSmallIntegerField(default=0)
    photo = models.ImageField(upload_to='',null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company'])
        ]
        ordering = [
            'name', 'company'
        ]


class Bgt(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='bgts', blank=True,null=True)
    name = models.CharField(max_length=25, default='بدون نام')
    company = models.CharField(max_length=25, default='personal')
    bg_price = models.PositiveIntegerField()
    amount = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    bg_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to='drugs', null=True,blank=True)
    bgt_bill = models.PositiveSmallIntegerField()
    unique = models.CharField(blank=True, unique=True, max_length=100)
    currency = models.CharField(default='AFS', max_length=3)
    sld_amount = models.PositiveSmallIntegerField(default=0, blank=True)  # this field increase in every sold

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company'])
        ]
        ordering = [
            'name', 'bgt_bill','bg_date'
        ]


class Sld(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE,
                             related_name='slds')  # we should also take out its bgts using this filed
    name = models.CharField(default='بدون نام',max_length=30)
    amount = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    sld_date = models.DateField(default=timezone.now)
    company = models.CharField(default='بدون شرکت',max_length=30)
    profite = models.IntegerField(blank=True)
    sld_bill = models.IntegerField()
    currency = models.CharField(default='AFS', max_length=3)
    unique = models.CharField(blank=True, max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name', 'sld_date', 'sld_bill']
