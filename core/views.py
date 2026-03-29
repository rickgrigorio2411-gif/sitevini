from django.shortcuts import render
from catalogo.models import Maquina, Categoria


def home(request):
    destaques = Maquina.objects.filter(disponivel=True, destaque=True)[:6]
    recentes = Maquina.objects.filter(disponivel=True).order_by('-criado_em')[:4]
    categorias = Categoria.objects.all()
    return render(request, 'core/home.html', {
        'destaques': destaques,
        'recentes': recentes,
        'categorias': categorias,
    })


def sobre(request):
    return render(request, 'core/sobre.html')


def contato(request):
    enviado = False
    if request.method == 'POST':
        enviado = True
    return render(request, 'core/contato.html', {'enviado': enviado})