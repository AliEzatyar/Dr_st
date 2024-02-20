from django.contrib.auth.decorators import login_required
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
    if request.method == 'POST':
        data = request.POST
        form = BgtForm(data)
        if form.is_valid():
            bgt = form.save()
            drug = Drug.objects.get_or_create(name=bgt.name, company=bgt.comapny)
            drug.existing_amount += bgt.amount
            drug.photo = bgt.photo
            drug.save()
            return HttpResponse('success')
    else:
        form = BgtForm(request.GET)
    return HttpResponse('started')
