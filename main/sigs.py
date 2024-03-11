from django.core.signals import request_started, request_finished
from django.db.backends.signals import connection_created
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Sld


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
def finished(*args,**kwargs):
    print("request finished")


@receiver(connection_created)
def created(*args,**kwargs):
    print("connection created!!!!!!!!!!!!!!!!!!!!!!!")




