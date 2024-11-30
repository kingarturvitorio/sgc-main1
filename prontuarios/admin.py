from django.contrib import admin
from . import models
# Register your models here.

class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('event', 'prontuario',)
    search_fiels = ('event',)

admin.site.register(models.Prontuario, ProntuarioAdmin)