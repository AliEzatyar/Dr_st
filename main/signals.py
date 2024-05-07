import os

from django.core.signals import request_started, request_finished
from django.db.backends.signals import connection_created
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from DrugStore import settings
from DrugStore.settings import BASE_DIR
from .models import Sld, Bgt, Drug


# @receiver(request_started)
# def started(*args, **kwargs):
#     print("request was made up")
#
#
# @receiver(request_finished)
# def finished(*args, **kwargs):
#     print("request finished")
#
#
# @receiver(connection_created)
# def created(*args, **kwargs):
#     print("connection created!!!!!!!!!!!!!!!!!!!!!!!")


@receiver(pre_delete, sender=Sld)
def sld_deletion(instance, *args, **kwargs):
    """instance is the object which is being deleted"""
    instance.bgt.sld_amount -= instance.amount
    instance.bgt.baqi_amount += instance.amount
    if instance.bgt.available == False:
        instance.bgt.available = True
    instance.drug.existing_amount += instance.amount
    instance.drug.save()
    instance.bgt.save()


@receiver(pre_delete, sender=Bgt)
def bgt_deletion(instance, *args, **kwargs):
    instance.drug.existing_amount -= instance.amount
    instance.drug.save()


@receiver(pre_delete, sender=Drug)
def drug_deletion(instance, *args, **kwargs):
    instance.photo.delete()


@receiver(post_save, sender=Sld)
def make_bgt_unavailable(instance, *args, **kwargs):
    bgt = instance.bgt
    if bgt.baqi_amount == 0:
        bgt.available = False
        bgt.save()


@receiver(post_save,sender=Bgt)
def rename_slds(instance,*args,**kwargs):
    """
        When a bgt is renamed, all related slds should be renamed too
    """
    bgt = instance
    try:
        pre_name = bgt.slds.all()[0]
    except:
        return 0
    if pre_name.name != bgt.name:
        print(pre_name, bgt.name)
        print("name changes")
        for sld in bgt.slds.all():
            sld.name = bgt.name
            sld.company = bgt.company
            sld.save()

@receiver(post_save,sender=Drug)
def set_defualt_photo(instance,*args,**kwargs):
    """
        if no photo was supplied initially for a drug, set BedonAks
    """
    if instance.photo in (None,""):
        print(settings.MEDIA_ROOT+"drugs")
        os.chdir(settings.MEDIA_ROOT+"drugs/")
        with open("BedonAks.jpg","rb") as file:
            instance.photo.save(instance.name+"__"+instance.company+".jpg",file,save=True)










