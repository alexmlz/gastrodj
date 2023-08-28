from django.urls import include, path

from . import views

urlpatterns = [
    path('<domainname>/journals/', views.journal_list, name='journal_list'),
    path('<domainname>/journal/<int:journal_id>/', views.journal, name='journal'),
    path('<domainname>/journaltest/<int:journal_id>/', views.journaltest, name='journal'),
    path('<domainname>/users/', views.UserCreate.as_view(), name='account-create'),
    path('<domainname>/login/', views.CustomAuthToken.as_view(), name='account-login'),
    path('<domainname>/logintest/', views.UserLogin.as_view(), name='login'),
    path('<domainname>/register/', views.UserRegister.as_view(), name='register'),
    path('<domainname>/logout/', views.UserLogout.as_view(), name='logout'),
    path('<domainname>/user/', views.UserView.as_view(), name='user'),
]
