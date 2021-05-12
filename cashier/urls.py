from django.urls import include, path

from . import views

urlpatterns = [
    path('<domainname>/products/', views.product_list, name='product_list'),
    path('<domainname>/products/<int:product_id>/', views.product_detail),
    path('<domainname>/nuggets/', views.nugget_list, name='nugget_list'),
    path('<domainname>/allnuggets/', views.nugget_list_all, name='nugget_list_all'),
    path('<domainname>/cats/', views.cat_list, name='cat_list'),
    path('<domainname>/optioncats/', views.option_cat_list, name='option_cat_list'),
    path('<domainname>/addons/', views.addon_list, name='addon_list'),
    path('<domainname>/baskets/', views.basket_list, name='basket_list'),
    path('<domainname>/baskets/<int:folg_id>/', views.basket_details, name='basket_details'),
    path('<domainname>/editbasket/<int:basket_id>/', views.basket_addon_edit, name='basket_addon_edit'),
    path('<domainname>/folg/', views.folg_list, name='folg_list'),
    path('<domainname>/basketcount/<int:folg_id>/', views.basket_count, name='basket_count'),
    path('<domainname>/folgTotal/<int:folg_id>/', views.folg_total, name='folg_total'),

]