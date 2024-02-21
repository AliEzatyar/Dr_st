from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from main.forms import BgtForm
from main.models import Drug


@login_required
def main(request):
    print('login was correct')
    print(request.GET)
    return render(request, 'main__/home.html', {'user': request.user})


@login_required
def buy(request):
    print("we are in buy view")
    if request.method == 'POST':
        data = request.POST
        form = BgtForm(data, request.FILES)
        if form.is_valid():
            bgt = form.save(commit=False)
            try:
                drug = Drug.objects.get(name=bgt.name, company=bgt.comapny)
                bgt.drug = drug
                drug.existing_amount += bgt.amount  # though we can get it by calling
                bgt.save()
                drug.save()
            except Drug.DoesNotExist:
                drug = Drug.objects.create(name=bgt.name, company=bgt.comapny)
                drug.photo = bgt.photo
                bgt.drug = drug
                drug.existing_amount += bgt.amount  # though we can get it by calling
                bgt.save()
                drug.save()

            messages.success(request, 'Saving was successful')
            return render(request,'buy/bgt.html',{'form':BgtForm()})
    else:
        form = BgtForm()
    print('we are rendering', form.data)
    return render(request, 'buy/bgt.html', {'form': form})
