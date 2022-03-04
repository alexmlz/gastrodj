from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.UserCreate.as_view(), name='account-create'),
    path('api/login/', views.CustomAuthToken.as_view(), name='account-login'),
]
