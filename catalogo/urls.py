from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_maquinas, name='lista'),
    path('<slug:slug>/', views.detalhe_maquina, name='detalhe'),
]