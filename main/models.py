import os
from django.db import models
from datetime import date

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django_jalali.db import models as jmodels


# Create your models here.


class Drug(models.Model):
    name = models.CharField(max_length=25, default="بدون نام")
    company = models.CharField(max_length=25)
    existing_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    photo = models.ImageField(upload_to='drugs/', null=True, default="static\\UsedPhoto\\BedonAks.jpg")
    description = models.TextField(blank=True, default="بدون جزئیات")
    unique = models.CharField(max_length=60, blank=True, default="no name and company", unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['name']),
            models.Index(fields=['company'])
        ]
        ordering = ['name', '-created']

    def __str__(self):
        return f"دارو با نام : {self.name} و با تعداد موجودی {self.existing_amount}"

    def get_absolute_url(self):
        return reverse("main:show_drug_detail", args=[self.name, self.company])


class Bgt(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='bgts', blank=True)
    name = models.CharField(max_length=25, default='بدون نام')
    company = models.CharField(max_length=25, default='بدون شرکت')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    created = jmodels.jDateTimeField(auto_now_add=True)
    date = jmodels.jDateField(default=jmodels.timezone.now())

    photo = models.ImageField(upload_to='drugs', null=True, blank=True)
    bgt_bill = models.PositiveSmallIntegerField(default=0)
    unique = models.CharField(blank=True, unique=True, max_length=100)
    currency = models.CharField(default='AFS', max_length=3)
    sld_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10,
                                     blank=True)  # this field increase in every sold
    baqi_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10, blank=True)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    available = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company']),
            models.Index(fields=['-date'])
        ]
        ordering = ['-name']

    def __str__(self):
        return f"{str(self.date)}|{self.amount}x|{self.price}"

    def get_absolute_url(self):
        return reverse('main:show_bgt_detail', args=[self.name, self.company, str(self.date)])


class Sld(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE,
                             related_name='slds')  # we should also take out its bgts using this filed
    bgt = models.ForeignKey(Bgt, on_delete=models.CASCADE, related_name="slds")
    name = models.CharField(default='بدون نام', max_length=30)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    created = jmodels.jDateTimeField(auto_now_add=True)
    date = jmodels.jDateField(default=jmodels.timezone.now())
    company = models.CharField(default='بدون شرکت', max_length=30)
    customer = models.CharField(default="نا مشخص", max_length=30)
    profite = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    sld_bill = models.IntegerField(default=0)
    currency = models.CharField(default='AFS', max_length=3, blank=True)
    unique = models.CharField(blank=True, max_length=100, unique=True)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-date'])
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} با تعداد {self.amount} فروش "

    def get_absolute_url(self):
        return reverse('main:show_sld_detail', args=[self.name, self.company, self.date, self.customer])


@receiver(pre_save, sender=Sld)
def before_sld_save(*args, **kwargs):
    print("before saving ")


@receiver(post_save, sender=Sld)
def after_sld_save(*args, **kwargs):
    print("after saving")
