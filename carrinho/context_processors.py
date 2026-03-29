from .models import Carrinho

def carrinho_context(request):
    quantidade = 0
    if request.session.session_key:
        try:
            carrinho = Carrinho.objects.get(session_key=request.session.session_key)
            quantidade = carrinho.quantidade_total
        except Carrinho.DoesNotExist:
            pass
    return{'carrinho_quantidade': quantidade}