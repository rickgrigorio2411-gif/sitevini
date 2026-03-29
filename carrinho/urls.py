from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.ver_carrinho, name='ver'),
    path('adicionar/<int:maquina_id>/', views.adicionar, name='adicionar'),
    path('remover/<int:item_id>/', views.remover, name='remover'),
    path('atualizar/<int:item_id>/', views.atualizar, name='atualizar'),
    path('checkout/', views.checkout, name='checkout'),
]
