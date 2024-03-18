from django.contrib import admin

# Register your models here.
from a_ccount.models import Prof
from main.models import Drug, Bgt, Sld




@admin.register(Bgt)
class BgtAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'price', 'amount','available', 'date', 'bgt_bill', 'unique', 'currency']
    list_filter = ['currency', 'date', 'company']
    ordering = [
        'name', 'bgt_bill', 'date'
    ]
    sortable_by = ['date','name','bgt_bill','amount']


@admin.register(Sld)
class SldAdmin(admin.ModelAdmin):
    list_display = ['name', 'company',"customer",'price', 'amount', 'date', 'sld_bill',"bgt", 'unique', 'currency']
    list_filter = ['currency', 'date', 'company',"bgt"]
    ordering = ['name', 'date', 'sld_bill']
    sortable_by = ['date','name','sld_bill','amount']

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'description','existing_amount']
    list_filter = ['company']
    sortable_by = ['name','existing_amount']
