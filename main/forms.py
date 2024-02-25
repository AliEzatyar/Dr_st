from datetime import datetime
from django_jalali.forms import jDateInput
from django_jalali.db import models as jmodels
from django_jalali.forms import forms as jforms
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from hijri_converter import Gregorian, Hijri
from main.models import Bgt, Sld


class HijriField(forms.DateField):
    class APShamsiDateField(forms.DateField):
        def to_python(self, value):
            if value in self.empty_values:
                return None

            if isinstance(value, str):
                try:
                    # Convert AP Shamsi date to Gregorian date
                    hijri = Hijri(value)
                    return super().to_python(hijri.to_gregorian())
                except ValueError:
                    raise forms.ValidationError('لطفا تاریخ شمسی درست وارد کنید')

            return super().to_python(value)

        def prepare_value(self, value):
            if isinstance(value, datetime.date):
                try:
                    # Convert Gregorian date to AP Shamsi date
                    gregorian = Gregorian(value.year, value.month, value.day)
                    hijri = gregorian.to_hijri()
                    print("higjroooooooooooo", hijri)
                    return hijri.__str__()
                except ValueError:
                    pass

            return super().prepare_value(value)


class BgtForm(forms.ModelForm):
    class Meta:
        model = Bgt
        fields = [  # fields which are not shown in template, 1- drug,2- sld_amount, 3- date, 4- unique
            'name', 'amount', 'bg_price', 'company', 'bg_date',
            'photo', 'bgt_bill', 'total', 'currency',
        ]

    def clean_price(self):
        cd = self.cleaned_data
        if int(cd['price']) > 15000:
            raise ValidationError('قیمت خرید منطقی نیست')

    def save(self, commit=True):
        """
            creating the unique, evaluating baqi capitalizing drug name and company
        """
        cd = self.cleaned_data
        bgt = super().save(commit=False)
        bgt.baqi_amount = cd['amount']
        bgt.name = cd['name'].title()
        bgt.comapny = cd['company'].title()
        bgt.unique = bgt.name + "&&" + str(cd['bg_date'])

        if commit:
            bgt.save()
        return bgt


class SldForm(forms.ModelForm):
    bgt_detail = forms.CharField(max_length=50)
    # sld_date = jforms.DateField()

    class Meta:
        model = Sld
        fields = [  # how to eclude??, excluded: drug,
            'name', 'amount', 'price', 'company',
            'sld_bill', 'currency', 'total','sld_date'
        ]

    def clean_price(self):
        cd = self.cleaned_data
        if int(cd['price']) > 15000:
            raise ValidationError("قیمت فروش منطقی نیست")
        return cd['price']

    # def clean_bgt_detail(self):
    #     returns the unique of the bgt object for further uses
    # cd = self.cleaned_data
    # bg_date = cd['bgt_detail'].split('|')[0].split()[0]
    # bgt = Bgt.objects.get(unique=cd['name']+"&&"+bg_date)
    # return bgt.unique
    # def clean_bgt(self):
    #     print("clean was called ")
    #     cd = self.cleaned_data
    #     bgt_str = cd['bgt']
    #     print("-------------------------",bgt_str)
    def clean(self):
        """in addition to clean, we are cleaning amount field for limiting max sale amount for a bgt"""
        cd = super().clean()

        if cd['name'] == "انتخاب دارو":
            raise ValidationError("لطفا دارو را انتخاب کنید")
        if cd['bgt_detail'] == "انتخاب خرید":
            raise ValidationError("لطفا یک خری را انتخاب کنید")
        if cd['company'] == "کمپنی دارو":
            raise ValidationError("لطفا کمپنی دارو را انتخاب کنید")

        bgt_date = cd['bgt_detail'].split("|")[0].split()[0]
        print("unique>", str(cd['name']).title() + "&&" + bgt_date)

        bgt_obj = Bgt.objects.get(unique=str(cd['name']).title() + "&&" + bgt_date)
        # limiting max sale amount
        remaining = bgt_obj.amount - bgt_obj.sld_amount
        sale_amount = cd['amount']
        if sale_amount == 0:
            raise ValidationError("مقدار فروش نادرست")
        if remaining - sale_amount < 0:
            raise ValidationError(f"در خرید این دارو بیشتر از {remaining} عدد باقی نمانده است!")
        return cd

    def save(self, commit=True):
        cd = self.cleaned_data
        sld_obj = super().save(commit=False)
        sld_obj.unique = str(cd['name']) + "&&" + str(cd['sld_date'])
        sld_obj.name, sld_obj.company = str(cd['name']).title(), str(cd['company']).title()
        if commit:
            sld_obj.save()
        return sld_obj
