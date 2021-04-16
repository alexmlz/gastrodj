from django.urls import include, path

from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail),
    path('nuggets/', views.nugget_list, name='nugget_list'),
    path('cats/', views.cat_list, name='cat_list'),

]