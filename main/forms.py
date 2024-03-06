from django import forms
from django.core.exceptions import ValidationError
from main.models import Bgt, Drug
from main.models import Sld


class BgtForm(forms.ModelForm):
    class Meta:
        model = Bgt
        fields = [  # fields which are not shown in template, 1- drug,2- sld_amount, 3- date, 4- unique
            'name', 'amount', 'bg_price', 'company', 'date',
            'photo', 'bgt_bill', 'total', 'currency',
        ]

    def clean_total(self):
        total = self.cleaned_data['total']
        return abs(total)

    def clean_bgt_bill(self):
        bill = self.cleaned_data['bgt_bill']
        return abs(bill)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return abs(amount)

    def clean_bg_price(self):
        price = self.cleaned_data['bg_price']
        return abs(price)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.title()

    def clean_company(self):
        company = self.cleaned_data['company']
        return company.title()

    def clean(self):
        cd = super().clean()
        """raising validation errors"""
        print(cd)
        name = cd['name']
        if name == "انتخاب دارو":
            raise ValidationError("لطفا نام دارو را درج کنید")

        company = self.cleaned_data['company']
        if company in "انتخاب شرکت":
            raise ValidationError("لطفا شرکت دارو را درج کنید")

        amount = int(cd['amount'])
        if amount == 0 or amount > 10000:
            raise ValidationError("مقدار خرید منطقی نیست")

        price = int(cd['bg_price'])
        if price > 15000 or price == 0:
            raise ValidationError('قیمت خرید منطقی نیست')

        bill = int(cd['bgt_bill'])
        if bill == 0:
            raise ValidationError("بیل نمبر درست نیست")

        unique = cd['name'].title() + "&&" + cd['company'].title() + "&&" + str(cd['date'])
        if Bgt.objects.filter(unique=unique).count() > 0:
            raise ValidationError("این خرید قبلا ثبت شده است")

        return cd

    def save(self, commit=True):
        """
            creating the unique, filling drug foriegnKey,evaluating baqi capitalizing drug name and company
        """
        cd = self.cleaned_data
        bgt = super().save(commit=False)
        bgt.baqi_amount = cd['amount']
        bgt.name = cd['name'].title()
        bgt.company = cd['company'].title()
        bgt.unique = bgt.name + "&&" + bgt.company + "&&" + str(cd['date'])
        # renaming image
        photo = cd['photo']
        """note: photos could be 2 type here, one is the default photo abs BedonAks, second: imageFiled object"""
        print(photo,"--++---------------------")
        if type(photo) != str:
            extension = str(photo.name).rsplit(".", 1)[1].lower()
            new_photo_name = bgt.name + "___" + bgt.company + "." + extension
            bgt.photo.name = new_photo_name
        if commit:
            bgt.save()
        return bgt


class SldForm(forms.ModelForm):
    bgt_detail = forms.CharField(max_length=50)

    class Meta:
        model = Sld
        fields = [  # how to eclude??, excluded: drug,
            'name', 'amount', 'price', 'company', 'customer',
            'sld_bill', 'currency', 'total', 'date'
        ]

    def clean_total(self):
        total = self.cleaned_data['total']
        return abs(total)

    def clean_sld_bill(self):
        bill = self.cleaned_data['sld_bill']
        return abs(bill)

    def clean_customer(self):
        customer = self.cleaned_data['customer']
        return customer.title()

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return abs(amount)

    def clean_price(self):
        price = self.cleaned_data['price']
        return abs(price)

    def clean_company(self):
        company = self.cleaned_data['company']
        return company.title()

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.title()

    def clean(self):
        """in addition to clean, we are cleaning amount field for limiting max sale amount for a bgt"""
        cd = super().clean()

        # raising form errors if needed
        name = cd['name']
        if name == "انتخاب دارو":
            raise ValidationError("لطفا دارو را انتخاب کنید")
        company = cd['company']
        if company == "شرکت دارو":
            raise ValidationError("لطفا شرکت دارو را انتخاب کنید")
        bgt_detail = cd["bgt_detail"]
        if bgt_detail == "انتخاب خرید":
            raise ValidationError("لطفا یک خرید را انتخاب کنید")
        price = cd['price']
        if price > 15000 or price == 0:
            raise ValidationError("قیمت فروش منطقی نیست")

        # finding the bgt object to limit exact bgt over-amount selling
        bgt_date = cd['bgt_detail'].split("|")[0].split()[0]
        bgt_unique = cd['name'] + "&&" + cd['company'] + "&&" + bgt_date
        bgt_obj = Bgt.objects.get(unique=bgt_unique)

        # preventing repetition of the same sale
        sld_unique = name + "&&" + str(cd['date']) + "&&" + cd['customer']
        if Sld.objects.filter(unique=sld_unique).count() > 0:
            raise ValidationError("این فروش قبلا ثبت شده است")

        # limiting max sale amount
        remaining = bgt_obj.amount - bgt_obj.sld_amount
        sale_amount = cd['amount']
        if sale_amount == 0:
            raise ValidationError("مقدار فروش نادرست")
        if remaining - sale_amount < 0:
            raise ValidationError(f"در خرید این دارو فقط{remaining} عدد باقی مانده است!")
        return cd

    def save(self, commit=True):
        """filling drug foriegnKey and creating unique"""
        cd = self.cleaned_data
        sld_obj = super().save(commit=False)
        sld_obj.unique = cd['name'] + "&&" + str(cd['date']) + "&&" + cd['customer']
        sld_obj.drug = Drug.objects.get(unique=sld_obj.name+"&&"+sld_obj.company)
        if commit:
            sld_obj.save()
        return sld_obj
