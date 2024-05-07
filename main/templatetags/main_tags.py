from django import template
from ..models import Sld, Bgt

register = template.Library()


@register.simple_tag(name="last_sale")
def last_sale(drug_name, company):
    sales = Sld.objects.filter(name=drug_name, company=company).order_by('-date')
    if len(sales) > 0:
        sale = sales[0]
        return sale
    else:
        return "ندارد"

@register.simple_tag(name="last_bgt")
def last_bgt(drug_name, company):
    bgts = Bgt.objects.filter(name=drug_name,company=company)
    bgt = bgts.order_by("-date")[0]
    return bgt
