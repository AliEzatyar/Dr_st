from io import BytesIO

import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from copy import deepcopy
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from .accessories import resize
from main.forms import BgtForm, SldForm, BgtEditForm, SldEdit, DrugEditForm
from main.models import Drug as Drg, Bgt, Sld
from main.models import Bgt as Bg
from django.db.backends.sqlite3.base import IntegrityError
from django.db.models.signals import post_save


def send_all_in_email(instance, request):
    print("semi-signal was called in checkforpdf signal", request, "-------------", )
    if request.session.get("CurrentCustomer") == instance.customer:
        # if this sale's customer is the current customer, add the new sale object id to the session
        if request.session.get(request.session.get("CurrentCustomer"), None):
            request.session[request.session.get("CurrentCustomer")][instance.id] = instance.id
        else:
            # if it has no sales yet, the initialize it to avoid Dict Error
            request.session['CurrentCustomer'] = instance.customer
            request.session[request.session['CurrentCustomer']] = {instance.id: instance.id}
    else:
        # if the current customer in the session is different from the one  of the new sale object,
        # it means the current customer is new and the previous sales should be sent via email and the new be initialiezed
        if request.session.get(request.session.get("CurrentCustomer"), None):
            # if the previous customer is not None, at least one sale had
            current_cus_sales = Sld.objects.filter(id__in=request.session[request.session.get("CurrentCustomer")])
            slds = current_cus_sales
            # creating the pdf
            html_str = render_to_string("sld/pdf_sld.html", {'slds': slds,"pdf":"ok"})
            bytes_io = BytesIO()

            weasyprint.HTML(string=html_str).write_pdf(bytes_io, stylesheets=[
                settings.STATIC_ROOT / "css/sld/sld.css"
            ])
            print("pdf was created successfully")
            # sending the email
            mail = EmailMessage(instance.customer, f"{instance.customer}'s purchases from ahmadyar shop",
                                settings.EMAIL_HOST_USER, ["aliahmadyar10@gmail.com"], )
            mail.attach(f"{instance.customer}__{instance.id}.pdf",
                        bytes_io.getvalue(), "attachment/pdf")

            mail.send(fail_silently=False)

            print("email was sent")
            # reassigning the new customer bill to the session
            request.session['CurrentCustomer'] = instance.customer
            request.session[request.session['CurrentCustomer']] = {instance.id: instance.id}
            print("reassignment was done successfully?")
        else:
            # if it has no sales yet, the initialize it to avoid Dict Error
            request.session['CurrentCustomer'] = instance.customer
            request.session[request.session['CurrentCustomer']] = {instance.id: instance.id}

@login_required
def main_page(request):

    drugs = Drg.objects.all().order_by('name')
    # print(drugs[0].photo.path,"---------------++++++++++++++")
    # making a paginator
    paginated = Paginator(drugs, 10)
    requested_page = None

    if "page" in request.GET:
        requested_page = request.GET['page']
        try:
            page = paginated.page(requested_page)
        except EmptyPage:
            if "just_page" in request.GET:
                return HttpResponse("")
            page = paginated.page(paginated.num_pages)
        except PageNotAnInteger:
            page = paginated.page(1)
        if requested_page:
            return render(request, "main__/portion_list.html", {"page": page,"home":"ok"})
    else:
        page = paginated.page(1)
        return render(request, 'main__/home.html', {'user': request.user, 'page': page,"home":"ok"})

@login_required
def buy(request):
    drugs = [drug.name for drug in Drg.objects.all()]
    media_url = request.build_absolute_uri("/media/drugs/")
    if request.method == 'POST':
        data = request.POST
        form = BgtForm(data, request.FILES)
        if form.is_valid():
            bgt = form.save(commit=False)
            try:
                drug = Drg.objects.get(unique=bgt.name + "&&" + bgt.company)
                bgt.drug = drug
                drug.existing_amount += bgt.amount  # though we can get it by calling

                bgt.save()
                drug.save()
                print("resize doen--------------________++++")
            except Drg.DoesNotExist:
                drug = Drg.objects.create(name=bgt.name, company=bgt.company,
                                          photo=bgt.photo, unique=bgt.name + "&&" + bgt.company,
                                          existing_amount=bgt.amount)
                bgt.drug = drug
                bgt.save()
            messages.success(request, "جزئیات خرید موفقانه ثبت گردید.")
            return render(request, 'bgt/bgt.html',
                          {'form': BgtForm(data=request.POST), "media_url": media_url, "drugs": drugs})
        else:
            errors = form.error_class.as_text(form.errors).split("\n")[1:]  # taking out erros
            messages.error(request, "خطا در ثبت معلومات!")
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
        return JsonResponse(companies,
                            safe=False)  # safe false because we are sending something rather than dict(list)

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
            sld_obj.profite = (sld_obj.price - bgt.price) * sld_obj.amount
            bgt.save()
            drug.save()
            sld_obj.save()
            if not request.session.get(request.session.get("CurrentCustomer", None), None):
                request.session["CurrentCustomer"] = sld_obj.customer
            send_all_in_email(sld_obj, request)
            drugs = [drug.name for drug in Drg.objects.all()]
            messages.success(request, "جزئیات فروش موفقانه ثبت گردید.")
            return render(request,
                          'sld/sld.html',
                          {
                              'form': SldForm(data=request.POST),
                              'media_url': media_url,
                              'drugs': drugs,
                          })
        else:
            drugs = [drug.name for drug in Drg.objects.all()]
            errors = form.error_class.as_text(form.errors).split("\n")[1:]  # taking out erros
            messages.error(request, "خطا در ثبت معلومات!")
            return render(request, 'sld/sld.html',
                          {'form': form, "drugs": drugs, "media_url": media_url, 'errors': errors})
    else:
        form = SldForm()
        drugs = [drug.name for drug in Drg.objects.all()]
        return render(request, 'sld/sld.html', {'form': form, "media_url": media_url, 'drugs': drugs})

@login_required
def get_drug_bgts(request):
    """sends bgt details for sell template in bgt selector"""
    drug_name = request.GET['drug_name']
    company = request.GET['company']
    bgts = Bg.objects.filter(name=drug_name, company=company, available=True)
    bgts = [(drug.price, drug.baqi_amount, str(drug.date), drug.currency) for drug in bgts]
    return JsonResponse(bgts, safe=False)

@login_required
def get_drug_companies(request):
    drug_name = request.GET['drug_name']
    drug_name = drug_name.title()
    companies = [drug.company for drug in Drg.objects.filter(name=drug_name)]
    return JsonResponse(safe=False, data=companies)

@login_required
def set_sld_photo(request):
    data = request.GET
    name = data['name']
    company = data['company']
    drug = Drg.objects.get(name=name, company=company)
    return HttpResponse(drug.photo.url)

@login_required
def show_drug_detail(request, name, company):
    name = name.title()
    company = company.title()
    drug = Drg.objects.get(name=name, company=company)
    return render(request, "drug/drug_detail.html", {"drug": drug})

@login_required
def show_bgt_detail(request, name, company, date):
    name = name.title()
    company = company.title()
    unique = name + "&&" + company + "&&" + date

    bgt = Bgt.objects.get(unique=unique)
    drug = Drg.objects.get(name=name, company=company)
    return render(request, "bgt/bgt_detail.html", {"bgt": bgt, "drug": drug})

@login_required
def show_sld_detail(request, name, company, date, customer):
    name = name.title()
    customer = customer.title()
    unique = name + "&&" + company + "&&" + date + "&&" + customer
    sld = Sld.objects.get(unique=unique)
    drug = Drg.objects.get(name=name, company=sld.company)
    return render(request, "sld/sld_detail.html", {"sld": sld, "drug": drug})

@login_required
def edit_bgt(request, name, company, date):
    """
        things to cnsider here
        * drug uniqe , name , existing amount could change since being update
        * bgt bqi and uniques + could be change
    """
    data = request.POST
    pre_bgt_unique = name + "&&" + company + "&&" + date
    pre_bgt = deepcopy(Bgt.objects.get(unique=pre_bgt_unique))
    pre_drug = deepcopy(pre_bgt.drug)
    if request.method == "POST":
        bgt_edit_form = BgtEditForm(files=request.FILES, instance=deepcopy(pre_bgt), data=data)
        drug_edit_form = DrugEditForm(files=request.FILES, instance=deepcopy(pre_drug), data=data)
        if bgt_edit_form.is_valid() and drug_edit_form.is_valid():
            new_bgt = bgt_edit_form.save(commit=False)
            new_drug = drug_edit_form.save(commit=False)
            new_drug.existing_amount = pre_drug.existing_amount - pre_bgt.amount + new_bgt.amount
            new_bgt.baqi_amount += new_bgt.amount - pre_bgt.amount
            new_drug.save()
            new_bgt.drug = new_drug
            new_bgt.save()
            messages.success(request, "تغییرات موفقانه ثبت گردید.")
            return redirect(new_bgt.get_absolute_url())
        else:
            return HttpResponse("invalid", bgt_edit_form.errors)

    else:
        unique = name + "&&" + company + "&&" + date
        instance = Bgt.objects.get(unique=unique)
        edit_form = BgtEditForm(instance=instance)
        return render(request, "bgt/bgt.html", {'form': edit_form, "edit": "1", 'instance': instance})

@login_required
def edit_sld(request, name, company, date, customer):
    pre_unique = name + "&&" + company + "&&" + date + "&&" + customer
    pre_sld = deepcopy(Sld.objects.get(unique=pre_unique))
    if request.method == "POST":
        sld_edit_form = SldEdit(instance=Sld.objects.get(unique=pre_unique), data=request.POST)
        if sld_edit_form.is_valid():
            new_sld = sld_edit_form.save(commit=False)
            # calculating the existing amount both for drug and bgt
            bgt_baqi = pre_sld.bgt.baqi_amount
            new_sld.drug.existing_amount = pre_sld.drug.existing_amount + pre_sld.amount - new_sld.amount
            new_sld.bgt.baqi_amount = bgt_baqi + pre_sld.amount - new_sld.amount
            new_sld.bgt.sld_amount = new_sld.bgt.amount - new_sld.bgt.baqi_amount
            new_sld.bgt.save()
            new_sld.drug.save()
            new_sld.save()
            # pre_sld.delete() ---> does not work since memory reference are the same
            return redirect(new_sld.get_absolute_url())
        else:
            return HttpResponse("THere was a problem", sld_edit_form.errors)
    else:
        sld_edit_frm = SldEdit(instance=pre_sld)
        return render(request, "sld/sld.html", {"form": sld_edit_frm, "instance": pre_sld, "edit": "1"})

@login_required
def delete(request, name, company, date=None, customer=None):
    if customer:  # sld deletion
        Sld.objects.get(name=name, company=company, date=date, customer=customer).delete()
        return redirect(reverse("main:show_list", args=["sld"]))
    elif date:  # bgt deleiton
        bgt = Bgt.objects.get(name=name, company=company, date=date)
        drug = Drg.objects.get(name=name, company=company)
        # deleting related slds
        if len(drug.bgts.all()) == 1:  # if it is the only remaining bgt
            drug.delete()  # deletes both drug and bgt and sld
        elif len(drug.bgts.all()) > 1:  # if it is one of the collection
            bgt.delete()
            for sld in Sld.objects.filter(bgt=bgt):
                sld.delete()
        return redirect(reverse("main:show_list", args=["bgt"]))
    else:  # Drug deleltion
        Drg.objects.get(name=name, company=company).delete()
        return redirect("main:main")

@login_required
def show_list(request, list_type):
    data = request.GET
    type = data.get("sort_by", "-date")
    if list_type == "bgt":
        bgts = Bgt.objects.all().order_by(type)
        return render(request, "bgt/list.html", {'bgts': bgts})
    else:
        slds = Sld.objects.all().order_by(type)
        return render(request, "sld/list.html", {'slds': slds})

@login_required
def show_specific(request, list_type):
    data = request.GET['data'].split("&&")
    name, company = data[0], data[1]
    if list_type == "bgt":
        bgts = Bgt.objects.filter(name=name,
                                  company=company).order_by('-date')
        return render(request, "bgt/list.html", {'bgts': bgts})
    else:
        slds = Sld.objects.filter(name=name,
                                  company=company).order_by('-date')
        return render(request, "sld/list.html", {'slds': slds})
