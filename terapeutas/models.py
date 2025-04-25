from django.db import models
import random
# Create your models here.

def gerar_cor_aleatoria():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class Terapeuta(models.Model):
    nome_terapeuta = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    contato = models.CharField(max_length=100, blank=True, null=True)
    titulo_profissional = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    funcao = models.CharField(max_length=100, blank=True, null=True)
    acordo = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    registro_classe = models.CharField(max_length=100, blank=True, null=True)
    conselho_classe = models.CharField(max_length=100, blank=True, null=True)
    dados_bancarios = models.CharField(max_length=100, blank=True, null=True)
    documentos = models.ImageField(upload_to='documentos_terapeuta/', blank=True, null=True)
    outros = models.TextField(null=True, blank=True)

    # Campo de métrica para contar eventos
    metric_terapeuta = models.IntegerField(default=0, editable=False)

    cor = models.CharField(max_length=7, default="#FFFFFF")

    ##ajusta a condição de tempo para salvar o final trinta minutos depois do inicio da consulta
    def save(self, *args, **kwargs):

        # Gera uma cor aleatória se o campo estiver vazio
        if not self.cor or self.cor == "#FFFFFF":
            self.cor = gerar_cor_aleatoria()
            
        # Incrementa a métrica toda vez que um evento é criado
        if not self.pk:  # Se o evento é novo (não tem chave primária ainda)
            self.metric_terapeuta =+ 1

        super(Terapeuta, self).save(*args, **kwargs)

    class Meta:
        ordering = ['nome_terapeuta']
    
    def __str__(self):
        return self.nome_terapeuta