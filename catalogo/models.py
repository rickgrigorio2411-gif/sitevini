from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icone = models.CharField(max_length=50, default='🏗️')
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Maquina(models.Model):
    CONDICAO_CHOICES = [
        ('nova', 'Nova'),
        ('seminova', 'Seminova'),
        ('usada', 'Usada'),
    ]

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='maquinas')
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    condicao = models.CharField(max_length=20, choices=CONDICAO_CHOICES, default='nova')
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    descricao = models.TextField()
    especificacoes = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='maquinas/', blank=True, null=True)
    estoque = models.IntegerField(default=1)
    destaque = models.BooleanField(default=False)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Máquina'
        verbose_name_plural = 'Máquinas'
        ordering = ['nome']

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.nome}'

    def get_absolute_url(self):
        return reverse('catalogo:detalhe', args=[self.slug])

    @property
    def preco_atual(self):
        return self.preco_promocional if self.preco_promocional else self.preco

    @property
    def em_promocao(self):
        return self.preco_promocional is not None and self.preco_promocional < self.preco

    @property
    def desconto_percentual(self):
        if self.em_promocao:
            return int((1 - self.preco_promocional / self.preco) * 100)
        return 0
