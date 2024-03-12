from django.core.signals import request_started, request_finished
from django.db.backends.signals import connection_created
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Sld, Bgt, Drug
from django.db.models.signals import post_delete


# @receiver(pre_save,Sld)
# def before_sld_save(*args,**kwargs):
#     print("before saving ")
#
#
# @receiver(post_save,Sld)
# def after_sld_save(*args,**kwargs):
#     pre_save("after saving")

@receiver(request_started)
def started(*args, **kwargs):
    print("request was made up")


@receiver(request_finished)
def finished(*args, **kwargs):
    print("request finished")


@receiver(connection_created)
def created(*args, **kwargs):
    print("connection created!!!!!!!!!!!!!!!!!!!!!!!")


@receiver(pre_delete, sender=Sld)
def sld_deletion(instance, *args, **kwargs):
    """instance is the object which is being deleted"""
    instance.bgt.sld_amount -= instance.amount
    instance.bgt.baqi_amount += instance.amount
    instance.drug.existing_amount += instance.amount
    instance.drug.save()
    instance.bgt.save()


@receiver(pre_delete, sender=Bgt)
def bgt_deletion(instance, *args, **kwargs):
    instance.drug.existing_amount -= instance.amount
    instance.drug.save()





