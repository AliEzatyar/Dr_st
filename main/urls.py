from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('',views.main_page,name="main"),
    path('buy/', views.buy, name='bgt'),
    path('sell', views.sell, name="sld"),
    # js
    path('listAll/',views.all_drugs,name='get_all_drugs'),# in js
    path('listBgts/',views.get_drug_bgts,name='get_bgts'),# in js
    path('getCompanies/',views.get_drug_companies,name="get_companies"), # in js
    path("photo/",views.set_sld_photo,name="set_sld_photo"),
    # show details
    path('detail/<str:name>/<str:company>/',views.show_drug_detail,name="show_drug_detail"),
    path('bgt_detail/<str:name>/<str:company>/<str:date>/',views.show_bgt_detail,name="show_bgt_detail"),
    path('sld_detail/<str:name>/<str:company>/<str:date>/<str:customer>/', views.show_sld_detail, name="show_sld_detail"),
    # editing
    path('Bgtdit/<str:name>/<str:company>/<str:date>/',views.edit_bgt,name="edit_bgt"),
    path('SldEdit/<str:name>/<str:company>/<str:date>/<str:customer>',views.edit_sld,name="edit_sld"),
    # deleting
    path('delete-drug/<str:name>/<str:company>/',views.delete,name="delete_drug"),
    path("delete-bgt/<str:name>/<str:company>/<str:date>/",views.delete,name="delete_bgt"),
    path("delete-sld/<str:name>/<str:company>/<str:date>/<str:customer>/", views.delete, name="delete_sld"),
    # show lists of sales and purchases
    path("list/<str:list_type>/",views.show_list,name="show_list"),
    # show the list for a specifc drug or company
    path("all/<str:list_type>/",views.show_specific,name="show_specific"),


]
