from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('',views.main_page,name="main"),
    path('buy/', views.buy, name='bgt'),
    path('listAll/',views.all_drugs,name='get_all_drugs'),
    path('sell/',views.sell,name="sld"),
    path('listBgts/',views.get_drug_bgts,name='get_bgts'),
    path('getCompanies/',views.get_drug_companies,name="get_companies"),
    path('detail/<str:name>/<str:company>/',views.show_drug_detail,name="show_drug_detail"),
    path('bgt_detail/<str:name>/<str:company>/<str:date>/',views.show_bgt_detail,name="show_bgt_detail"),
    path('sld_detail/<str:name>/<str:customer>/<str:date>/', views.show_sld_detail, name="show_sld_detail"),

]
