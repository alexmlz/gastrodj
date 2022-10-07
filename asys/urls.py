from django.urls import path
from . import views

urlpatterns = [
    path('<domainname>/users/', views.UserCreate.as_view(), name='account-create'),
    path('<domainname>/login/', views.CustomAuthToken.as_view(), name='account-login'),
    path('<domainname>/test/', views.ExampleView.as_view(), name='test'),
    path('<domainname>/appointment/', views.AppointmentsView.as_view(), name='appointments'),
    path('<domainname>/appointmentpublic/', views.AppointmentsPublicView.as_view(), name='appointmentspublic'),
    path('<domainname>/utaint/', views.UtaIntView.as_view(), name='utaint'),
    path('<domainname>/thema/', views.ThemaView.as_view(), name='thema'),
    path('<domainname>/themasingle/<int:thema_id>/', views.ThemaSingleView.as_view(), name='themasingle'),
    path('<domainname>/agent/', views.AgentView.as_view(), name='agent'),
    path('<domainname>/checkuser/', views.CheckUserView.as_view(), name='checkuser'),
]
