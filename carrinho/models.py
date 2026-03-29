from django.db import models
from catalogo.models import Maquina


class Carrinho(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f'Carrinho {self.session_key}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    @property
    def quantidade_total(self):
        return sum(item.quantidade for item in self.itens.all())


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    class Meta:
        unique_together = ['carrinho', 'maquina']

    def __str__(self):
        return f'{self.quantidade}x {self.maquina.nome}'

    @property
    def subtotal(self):
        return self.maquina.preco_atual * self.quantidade


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    empresa = models.CharField(max_length=200, blank=True)
    endereco = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.nome}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True)
    nome_maquina = models.CharField(max_length=200)
    preco_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    quantidade = models.IntegerField()

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade