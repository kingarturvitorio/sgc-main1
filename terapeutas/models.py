from django.db import models

# Create your models here.

class Terapeuta(models.Model):
    nome_terapeuta = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    contato = models.CharField(max_length=100, blank=True, null=True)
    titulo_profissional = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)
    acordo = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    registro_classe = models.CharField(max_length=100, blank=True, null=True)
    conselho_classe = models.CharField(max_length=100, blank=True, null=True)
    dados_bancarios = models.CharField(max_length=100, blank=True, null=True)
    documentos = models.ImageField(upload_to='documentos_terapeuta/', blank=True, null=True)
    outros = models.TextField(null=True, blank=True)

    # Campo de métrica para contar eventos
    metric_terapeuta = models.IntegerField(default=0, editable=False)

    ##ajusta a condição de tempo para salvar o final trinta minutos depois do inicio da consulta
    def save(self, *args, **kwargs):

        # Incrementa a métrica toda vez que um evento é criado
        if not self.pk:  # Se o evento é novo (não tem chave primária ainda)
            self.metric_terapeuta = Terapeuta.objects.count() + 1

        super(Terapeuta, self).save(*args, **kwargs)

    class Meta:
        ordering = ['nome_terapeuta']
    
    def __str__(self):
        return self.nome_terapeuta