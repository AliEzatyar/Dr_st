from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('',views.main,name="main"),
    path('buy/', views.buy, name='bgt'),
    path('listAll/',views.all_drugs,name='get_all_drugs'),
    path('sell/',views.sell,name="sld"),
    path('listBgts/',views.get_drug_bgts,name='get_bgts'),
    path('getCompanies/',views.get_drug_companies,name="get_companies")
]
