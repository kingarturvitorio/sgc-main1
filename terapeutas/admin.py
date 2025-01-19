from django.contrib import admin
from . import models
# Register your models here.

class TerapeutaAdmin(admin.ModelAdmin):
    list_display = ('nome_terapeuta', 'email', 'contato', 'titulo_profissional', 
                    'tipo', 'funcao', 'acordo',
                    'valor', 'registro_classe', 'conselho_classe',
                    'dados_bancarios', 'documentos', 'outros', 'cor')
    search_fiels = ('nome_terapeuta',)

admin.site.register(models.Terapeuta, TerapeutaAdmin)