from django.contrib import admin
from django.contrib import admin
from . import models
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'terapeuta', 'cidade', 
                    'tipo_terapia', 'guia', 'start_time', 'end_time','descricao', 'confirmado')

admin.site.register(models.Event, EventAdmin)

