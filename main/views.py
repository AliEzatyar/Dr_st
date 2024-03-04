from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from main.forms import BgtForm, SldForm
from main.models import Drug as Drg, Bgt, Sld
from main.models import Bgt as Bg


@login_required
def main(request):
    x = Drg.objects.all()[0]

    return render(request, 'main__/home.html', {'user': request.user, 'durgs': Drg.objects.all()})


@login_required
def buy(request):
    drugs = [drug.name for drug in Drg.objects.all()]
    media_url = request.build_absolute_uri("/media/drugs/")
    if request.method == 'POST':
        data = request.POST
        form = BgtForm(data, request.FILES)
        print(request.POST)
        print("the from", form)
        if form.is_valid():
            bgt = form.save(commit=False)
            try:
                drug = Drg.objects.get(unique=bgt.name + "&&" + bgt.company)
                bgt.drug = drug

                drug.existing_amount += bgt.amount  # though we can get it by calling
                bgt.save()
                drug.save()
            except Drg.DoesNotExist:
                drug = Drg.objects.create(name=bgt.name, company=bgt.company,
                                          photo=bgt.photo, unique=bgt.name + "&&" + bgt.company,
                                          existing_amount=bgt.amount)
                bgt.drug = drug
                print("bgt_drig", bgt.drug)
                bgt.save()
            messages.success(request, 'Saving was successful')
            return render(request, 'bgt/bgt.html', {'form': BgtForm(), "media_url": media_url, "drugs": drugs})
        else:
            errors = form.error_class.as_text(form.errors).split("\n")[1:]  # taking out erros
            return render(request, 'bgt/bgt.html',
                          {'form': form, "drugs": drugs, "media_url": media_url, 'errors': errors})
    else:
        form = BgtForm()
    return render(request, 'bgt/bgt.html', {'form': form, 'drugs': drugs, "media_url": media_url})


@login_required
def all_drugs(request):
    """ sends the names of the drugs through fetch for select element"""
    if not 'company' in request:
        drugs = [drug.name for drug in Drg.objects.all()]
        return JsonResponse(drugs, safe=False)
    else:
        companies = [drug.company for drug in Drg.objects.filter(name=str(request['name']).title())]
        return JsonResponse(companies, safe=False)  # safe false because we are sending something rather than dict(list)


@login_required
def sell(request):
    media_url = request.build_absolute_uri("/media/drugs/")
    if request.method == "POST":
        """ save the image,  """
        form = SldForm(request.POST, request.FILES)

        if form.is_valid():
            sld_obj = form.save(commit=False)
            cd = form.cleaned_data
            drug = Drg.objects.get(unique=cd['name'].title() + "&&" + cd['company'].title())
            sld_obj.drug = drug
            drug.existing_amount -= sld_obj.amount
            # bgt object remaining amount calculations, profite calculation
            date = request.POST['bgt_detail'].split('|')[0].split()[0]  # since it was made in js and get_bgts
            bgt = Bg.objects.get(unique=cd['name'].title() + "&&" + cd['company'].title() + "&&" + date)
            bgt.sld_amount += sld_obj.amount
            bgt.baqi_amount -= cd['amount']  # updating baqi after each sell
            sld_obj.bgt = bgt
            sld_obj.profite = (sld_obj.price - bgt.bg_price) * sld_obj.amount
            bgt.save()
            drug.save()
            sld_obj.save()
            drugs = [drug.name for drug in Drg.objects.all()]
            messages.success(request, "معلومات موفقانه ذخیره گردید")
            return render(request, 'sld/sld.html', {'form': SldForm(), "media_url": media_url, 'drugs': drugs})
        else:
            drugs = [drug.name for drug in Drg.objects.all()]
            errors = form.error_class.as_text(form.errors).split("\n")[1:]  # taking out erros
            return render(request, 'sld/sld.html',
                          {'form': form, "drugs": drugs, "media_url": media_url, 'errors': errors})
    else:
        form = SldForm()
        drugs = [drug.name for drug in Drg.objects.all()]
        return render(request, 'sld/sld.html', {'form': form, "media_url": media_url, 'drugs': drugs})


@login_required
def get_drug_bgts(request):
    drug_name = request.GET['drug_name']
    company = request.GET['company']
    bgts = Bg.objects.filter(name=drug_name, company=company)
    bgts = [(drug.bg_price, drug.baqi_amount, str(drug.date), drug.currency) for drug in bgts]
    return JsonResponse(bgts, safe=False)


@login_required
def get_drug_companies(request):
    drug_name = request.GET['drug_name']
    drug_name = drug_name.title()
    companies = [drug.company for drug in Drg.objects.filter(name=drug_name)]
    return JsonResponse(safe=False, data=companies)


@login_required
def get_photo_url(request):
    name = request.GET['drug_name']
    company = request.GET['company']


@login_required
def show_drug_detail(request, name, company):
    name = name.title()
    company = company.title()
    drug = Drg.objects.get(name=name, company=company)
    return render(request, "drug/drug_detail.html", {"drug": drug})


@login_required
def show_bgt_detail(request, name, company, date):
    name = name.title()
    print("bgt_detai veiw")
    company = company.title()
    unique = name + "&&" + company + "&&" + date
    bgt = Bgt.objects.get(unique=unique)
    drug = Drg.objects.get(name=name, company=company)
    return render(request, "bgt/bgt_detail.html", {"bgt": bgt, "drug": drug})


@login_required
def show_sld_detail(request, name, customer, date):
    name = name.title()
    customer = customer.title()
    unique = name + "&&" + date + "&&" + customer
    sld = Sld.objects.get(unique=unique)
    drug = Drg.objects.get(name=name, company=sld.company)
    return render(request, "sld/sld_detail.html", {"sld": sld, "drug": drug})
