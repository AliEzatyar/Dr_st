from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from main.models import Bgt


class BgtForm(forms.ModelForm):
    class Meta:
        model = Bgt
        fields = [
            'name', 'amount', 'bg_price','company', 'bg_date',
            'photo', 'bgt_bill', 'currency',
        ]

    def clean_price(self):
        cd = self.cleaned_data
        if int(cd['price']) > 15000:
            raise ValidationError('عدد بزرگ است')

    def save(self, commit=True):
        cd = self.cleaned_data
        bgt = super().save(commit=False)
        bgt.unique = str(cd['name']) + "&&" + str(cd['bg_date'])
        bgt.name = cd['name'].title()
        bgt.comapny = cd['company'].title()

        if commit:
            bgt.save()
        return bgt
