from django.contrib import admin
from . import models
# Register your models here.

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carteirinha', 'documento', 'endereco', 'telefone_responsavel', 
                    'telefone_contato', 'telefone_emergencia', 'tipo_convenio',
                    'data_nascimento', 'nome_responsavel', 'documento_responsavel',
                    'foto_carteirinha',)
    search_fiels = ('nome',)

admin.site.register(models.Paciente, PacienteAdmin)