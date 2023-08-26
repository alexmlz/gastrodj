from django.urls import include, path

from . import views

urlpatterns = [
    path('<domainname>/journals/', views.journal_list, name='journal_list'),
    path('<domainname>/journal/<int:journal_id>/', views.journal, name='journal_list')
]
