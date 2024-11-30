from django.db import models
from terapeutas.models import Terapeuta
from pacientes.models import Paciente
from calendario.models import Event
# Create your models here.

class Prontuario(models.Model):

    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='event')
    prontuario = models.CharField(max_length=1000)
   
    def __str__(self):
        return f'{self.event}'
