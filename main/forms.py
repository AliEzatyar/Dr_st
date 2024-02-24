from datetime import datetime

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
                    gregorian = Gregorian(value.year,value.month,value.day)
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
    class Meta:
        model = Sld
        fields = [  # how to eclude??, excluded: drug,
            'name', 'amount', 'price', 'company', 'sld_date',
            'sld_bill', 'currency', 'total'
        ]

    def clean_price(self):
        cd = self.cleaned_data
        if int(cd['price']) > 15000:
            raise ValidationError("قیمت فروش منطقی نیست")
        return cd['price']

    def clean_amount(self):
        amount = self.cleaned_data['amount']

    # def clean_bgt_detail(self):
    #     x  = 8
    #     print("we are in bgt detail")

    # does not work for relationships
    def clean_bgt(self):
        print("clean was called ")
        cd = self.cleaned_data
        bgt_str = cd['bgt']
        print("-------------------------",bgt_str)

    def save(self, commit=True):
        cd = self.cleaned_data
        print(cd)
        print(cd['price'])
        sld_obj = super().save(commit=False)
        sld_obj.unique = str(cd['name']) + "&&" + str(cd['sld_date'])
        sld_obj.name, sld_obj.company = str(cd['name']).title(), str(cd['company']).title()
        if commit:
            sld_obj.save()
        return sld_obj

