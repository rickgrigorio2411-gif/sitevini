from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalogo.models import Maquina
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido


def get_or_create_carrinho(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    carrinho, _ = Carrinho.objects.get_or_create(session_key=session_key)
    return carrinho


def ver_carrinho(request):
    carrinho = get_or_create_carrinho(request)
    return render(request, 'carrinho/carrinho.html', {'carrinho': carrinho})


def adicionar(request, maquina_id):
    maquina = get_object_or_404(Maquina, pk=maquina_id)
    carrinho = get_or_create_carrinho(request)
    item, criado = ItemCarrinho.objects.get_or_create(carrinho=carrinho, maquina=maquina)
    if not criado:
        if item.quantidade < maquina.estoque:
            item.quantidade += 1
            item.save()
            messages.success(request, f'Quantidade de "{maquina.nome}" atualizada!')
        else:
            messages.warning(request, f'Estoque insuficiente!')
    else:
        messages.success(request, f'"{maquina.nome}" adicionado ao carrinho!')
    return redirect('carrinho:ver')


def remover(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id)
    nome = item.maquina.nome
    item.delete()
    messages.info(request, f'"{nome}" removido do carrinho.')
    return redirect('carrinho:ver')


def atualizar(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id)
    quantidade = int(request.POST.get('quantidade', 1))
    if quantidade > 0 and quantidade <= item.maquina.estoque:
        item.quantidade = quantidade
        item.save()
    elif quantidade <= 0:
        item.delete()
    return redirect('carrinho:ver')


def checkout(request):
    carrinho = get_or_create_carrinho(request)
    if not carrinho.itens.exists():
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('carrinho:ver')

    if request.method == 'POST':
        pedido = Pedido.objects.create(
            nome=request.POST['nome'],
            email=request.POST['email'],
            telefone=request.POST['telefone'],
            empresa=request.POST.get('empresa', ''),
            endereco=request.POST['endereco'],
            cidade=request.POST['cidade'],
            estado=request.POST['estado'],
            cep=request.POST['cep'],
            total=carrinho.total,
            observacoes=request.POST.get('observacoes', ''),
        )
        for item in carrinho.itens.all():
            ItemPedido.objects.create(
                pedido=pedido,
                maquina=item.maquina,
                nome_maquina=item.maquina.nome,
                preco_unitario=item.maquina.preco_atual,
                quantidade=item.quantidade,
            )
        carrinho.itens.all().delete()
        messages.success(request, f'Pedido #{pedido.pk} realizado com sucesso!')
        return redirect('core:home')

    return render(request, 'carrinho/checkout.html', {'carrinho': carrinho})

# Create your views here.
