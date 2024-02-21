from django.contrib import admin

# Register your models here.
from a_ccount.models import Prof
from main.models import Drug, Bgt, Sld




@admin.register(Bgt)
class BgtAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'bg_price', 'amount', 'bg_date', 'bgt_bill', 'unique', 'currency']
    list_filter = ['currency', 'bg_date', 'company']
    ordering = [
        'name', 'bgt_bill', 'bg_date'
    ]


@admin.register(Sld)
class SldAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'price', 'amount', 'sld_date', 'sld_bill', 'unique', 'currency']
    list_filter = ['currency', 'sld_date', 'company']
    ordering = ['name', 'sld_date', 'sld_bill']


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'description']
    list_filter = ['company']
