from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserCreate.as_view(), name='account-create'),
    path('login/', views.CustomAuthToken.as_view(), name='account-login'),
    path('test/', views.ExampleView.as_view(), name='test'),
    path('<domainname>/appointment/', views.AppointmentsView.as_view(), name='appointments'),
    path('<domainname>/appointmentpublic/', views.AppointmentsPublicView.as_view(), name='appointments'),
]
