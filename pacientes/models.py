from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    documento = models.CharField(max_length=100, blank=True, null=True)
    carteirinha = models.CharField(max_length=100, blank=True, null=True)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    telefone_responsavel = models.CharField(max_length=100, blank=True, null=True)
    telefone_contato = models.CharField(max_length=100, blank=True, null=True)
    telefone_emergencia = models.CharField(max_length=100, blank=True, null=True)
    tipo_convenio = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    nome_responsavel = models.CharField(max_length=100, blank=True, null=True)
    documento_responsavel = models.CharField(max_length=100, blank=True, null=True)
    foto_carteirinha = models.ImageField(upload_to='documentos_pacientes/', blank=True, null=True)

    # Campo de métrica para contar eventos
    metric_paciente = models.IntegerField(default=0, editable=False)

    ##ajusta a condição de tempo para salvar o final trinta minutos depois do inicio da consulta
    def save(self, *args, **kwargs):

        # Incrementa a métrica toda vez que um evento é criado
        if not self.pk:  # Se o evento é novo (não tem chave primária ainda)
            self.metric_paciente = Paciente.objects.count() + 1

        super(Paciente, self).save(*args, **kwargs)

    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome