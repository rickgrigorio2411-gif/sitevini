from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Maquina, Categoria


def lista_maquinas(request):
    maquinas = Maquina.objects.filter(disponivel=True)
    categorias = Categoria.objects.all()

    busca = request.GET.get('busca', '')
    condicao = request.GET.get('condicao', '')
    ordenar = request.GET.get('ordenar', '')
    categoria_slug = request.GET.get('categoria')

    categoria_atual = None
    if categoria_slug:
        categoria_atual = get_object_or_404(Categoria, slug=categoria_slug)
        maquinas = maquinas.filter(categoria=categoria_atual)

    if busca:
        maquinas = maquinas.filter(
            Q(nome__icontains=busca) |
            Q(marca__icontains=busca) |
            Q(modelo__icontains=busca)
        )

    if condicao:
        maquinas = maquinas.filter(condicao=condicao)

    if ordenar == 'menor_preco':
        maquinas = maquinas.order_by('preco')
    elif ordenar == 'maior_preco':
        maquinas = maquinas.order_by('-preco')
    elif ordenar == 'mais_novo':
        maquinas = maquinas.order_by('-ano')

    return render(request, 'catalogo/lista.html', {
        'maquinas': maquinas,
        'categorias': categorias,
        'categoria_atual': categoria_atual,
        'busca': busca,
        'condicao': condicao,
        'ordenar': ordenar,
    })


def detalhe_maquina(request, slug):
    maquina = get_object_or_404(Maquina, slug=slug, disponivel=True)
    relacionadas = Maquina.objects.filter(
        categoria=maquina.categoria, disponivel=True
    ).exclude(pk=maquina.pk)[:4]

    return render(request, 'catalogo/detalhe.html', {
        'maquina': maquina,
        'relacionadas': relacionadas,
    })

# Create your views here.
