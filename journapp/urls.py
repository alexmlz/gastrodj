from django.urls import include, path

from . import views

urlpatterns = [
    path('journals/', views.journal_list, name='journal_list'),
    path('journal/<int:journal_id>/', views.journal, name='journal'),
    path('users/', views.UserCreate.as_view(), name='account-create'),
    path('login/', views.CustomAuthToken.as_view(), name='account-login'),
    path('logintest/', views.UserLogin.as_view(), name='login'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('user/', views.UserView.as_view(), name='user'),
    path('useradmin/', views.UsersView.as_view(), name='users'),
    path('questions/', views.question_list, name='question_list'),
    path('question/', views.question, name='question'),
]
