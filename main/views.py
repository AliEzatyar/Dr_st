from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from main.forms import BgtForm, SldForm
from main.models import Drug, Bgt


@login_required
def main(request):
    return render(request, 'main__/home.html', {'user': request.user})


@login_required
def buy(request):
    if request.method == 'POST':
        data = request.POST
        form = BgtForm(data, request.FILES)
        if form.is_valid():
            bgt = form.save(commit=False)
            try:
                drug = Drug.objects.get(unique=bgt.name.title() + "&&" + bgt.company.title())
                bgt.drug = drug
                drug.existing_amount += bgt.amount  # though we can get it by calling
                bgt.save()
                drug.save()
            except Drug.DoesNotExist:
                drug = Drug.objects.create(name=bgt.name, company=bgt.company,
                                           photo=bgt.photo,unique=bgt.name.title() + "&&" + bgt.company.title(),
                                           existing_amount=bgt.amount)
                bgt.drug = drug
                bgt.save()

            messages.success(request, 'Saving was successful')
            return render(request, 'bgt/bgt.html', {'form': BgtForm()})
        return render(request, 'bgt/bgt.html', {"form": form, "errors": form.errors})
    else:
        form = BgtForm()
    return render(request, 'bgt/bgt.html', {'form': form})


@login_required
def all_drugs(request):
    """ sends the names of the drugs"""
    if not 'company' in request:
        drugs = [drug.name for drug in Drug.objects.all()]
        return JsonResponse(drugs, safe=False)
    else:
        companies = [drug.company for drug in Drug.objects.filter(name=str(request['name']).title())]
        return JsonResponse(companies, safe=False)  # safe false because we are sending something rather than dict(list)


@login_required
def sell(request):
    form = None
    if request.method == "POST":
        """ save the image,  """
        form = SldForm(request.POST, request.FILES)
        if form.is_valid():
            sld_obj = form.save(commit=False)
            cd = form.cleaned_data
            drug = Drug.objects.get(unique=cd['name'].title()+"&&"+cd['company'].title())
            sld_obj.drug = drug
            print("current existing ###",drug.existing_amount)
            drug.existing_amount -= sld_obj.amount
            print("current existing ###",drug.existing_amount)
            # bgt object remaining amount calculations, profite calculation
            bg_date = request.POST['bgt_detail'].split('|')[0].split()[0] # since it was made in js and get_bgts
            bgt = Bgt.objects.get(unique=cd['name'].title()+"&&"+bg_date)
            bgt.sld_amount += sld_obj.amount
            bgt.baqi_amount -= cd['amount'] # updating baqi after each sell
            sld_obj.bgt = bgt
            sld_obj.profite = (sld_obj.price - bgt.bg_price)*sld_obj.amount
            bgt.save()
            drug.save()
            sld_obj.save()
            drugs = [drug.name for drug in Drug.objects.all()]
            messages.success(request, "معلومات موفقانه ذخیره گردید")
            return render(request, 'sld/sld.html', {'form': SldForm(),'drugs':drugs})
        else:
            drugs = [drug.name for drug in Drug.objects.all()]
            errors = str(form.errors).split(">")[4].split("<")[0] # taking out erros
            return render(request, 'sld/sld.html', {'form': form,"drugs":drugs,'errors':errors})
    else:
        form = SldForm()
        drugs = [drug.name for drug in Drug.objects.all()]
        return render(request, 'sld/sld.html', {'form': form, 'drugs':drugs})



@login_required
def get_drug_bgts(request):
    drug_name = request.GET['drug_name']
    company = request.GET['company']
    bgts = Bgt.objects.filter(name=drug_name,company=company)
    bgts = [(drug.bg_price,drug.baqi_amount, str(drug.bg_date),drug.currency) for drug in bgts]
    return JsonResponse(bgts, safe=False)

@login_required
def get_drug_companies(request):
    drug_name = request.GET['drug_name']
    drug_name  = drug_name.title()
    companies = [drug.company for drug in Drug.objects.filter(name=drug_name)]
    return JsonResponse(safe=False,data=companies)






