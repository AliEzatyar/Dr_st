from django.db import models
from datetime import date
from django_jalali.db import models as jmodels
# Create your models here.
from django.utils import timezone


class Drug(models.Model):
    name = models.CharField(max_length=25, default="بدون نام")
    company = models.CharField(max_length=25)
    existing_amount = models.PositiveSmallIntegerField(default=0)
    photo = models.ImageField(upload_to='', null=True)
    description = models.TextField(blank=True, null=True)
    unique = models.CharField(max_length=60, blank=True, unique=True, default="no name and company", primary_key=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company'])
        ]
        ordering = [
            'name', 'company'
        ]

    def __str__(self):
        return f"دارو با نام : {self.name} و با تعداد موجودی {self.existing_amount}"


class Bgt(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='bgts', blank=True, null=True)
    name = models.CharField(max_length=25, default='بدون نام')
    company = models.CharField(max_length=25, default='بدون شرکت')
    bg_price = models.PositiveIntegerField(default=0)
    amount = models.PositiveSmallIntegerField(default=0)
    date =jmodels.jDateTimeField(auto_now_add=True)
    bg_date =jmodels.jDateField(default=jmodels.timezone.now())
    photo = models.ImageField(upload_to='drugs', null=True, blank=True)
    bgt_bill = models.PositiveSmallIntegerField(default=0)
    unique = models.CharField(blank=True, unique=True, max_length=100)
    currency = models.CharField(default='AFS', max_length=3)
    sld_amount = models.PositiveSmallIntegerField(default=0, blank=True)  # this field increase in every sold
    baqi_amount = models.PositiveSmallIntegerField(default=0, blank=True)
    total = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company'])
        ]
        ordering = [
            'name', 'bgt_bill', 'bg_date'
        ]

    def __str__(self):
        return f"{self.name} با تعداد {self.amount} خرید شد"


class Sld(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE,
                             related_name='slds')  # we should also take out its bgts using this filed
    bgt = models.ForeignKey(Bgt, on_delete=models.CASCADE, related_name="slds")
    name = models.CharField(default='بدون نام', max_length=30)
    amount = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    date = jmodels.jDateTimeField(auto_now_add=True)
    sld_date = jmodels.jDateField(default=jmodels.timezone.now())
    company = models.CharField(default='بدون شرکت', max_length=30)
    profite = models.IntegerField(blank=True)
    sld_bill = models.IntegerField(default=0)
    currency = models.CharField(default='AFS', max_length=3, blank=True)
    unique = models.CharField(blank=True, max_length=100)
    total = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name', 'sld_date', 'sld_bill']

    def __str__(self):
        return f"{self.name} با تعداد {self.amount} فروخته شد"
