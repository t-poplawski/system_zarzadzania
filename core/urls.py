from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:rok>/<str:tabela>/', views.tabela_view, name='tabela_view'),
]