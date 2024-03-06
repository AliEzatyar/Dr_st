from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Sld


@receiver(pre_save,Sld)
def before_sld_save(*args,**kwargs):
    print("before saving ")


@receiver(post_save,Sld)
def after_sld_save(*args,**kwargs):
    pre_save("after saving")
