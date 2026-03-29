from django.contrib import admin
from .models import Maquina, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'icone']
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'marca', 'modelo', 'ano', 'preco', 'condicao', 'estoque', 'destaque', 'disponivel']
    list_filter = ['categoria', 'condicao', 'destaque', 'disponivel']
    list_editable = ['preco', 'estoque', 'destaque', 'disponivel']
    search_fields = ['nome', 'marca', 'modelo']
    prepopulated_fields = {'slug': ('nome',)}
    
# Register your models here.
