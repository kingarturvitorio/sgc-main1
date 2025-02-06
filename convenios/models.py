from django.db import models

# Create your models here.

class Convenio(models.Model):
    nome_convenio = models.CharField(max_length=100)
    numero_convenio = models.CharField(max_length=100, blank=True, null=True)
    informacoes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['nome_convenio']
    
    def __str__(self):
        return self.nome_convenio