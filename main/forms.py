from django import forms
from django.core.exceptions import ValidationError

from main.models import Bgt


class BgtForm(forms.ModelForm):
    class Meta:
        model = Bgt
        fields = ['name', 'amount', 'price', 'company', 'bg_date', 'photo', 'bgt_bill', 'currency', 'sld_amount']

    def clean_price(self):
        cd = self.cleaned_data
        if int(cd['price']) > 15000:
            raise ValidationError('عدد بزرگ است')

    def save(self, commit=True):
        cd = self.cleaned_data
        bgt = super().save(commit=False)
        bgt.unique = str(cd['name']) + "&&" + str(cd['date'])
        bgt.name = cd['name'].title()
        bgt.comapny = cd['comapny'].title()
        bgt.photo.save(str(bgt.name + "__" + bgt.comapny), save=False)
        if commit:
            bgt.save()
        return bgt
