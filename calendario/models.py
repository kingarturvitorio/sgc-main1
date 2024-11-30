from django.db import models
from pacientes.models import Paciente
from terapeutas.models import Terapeuta
# Create your models here.
from datetime import datetime
from usuarios.models import User
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

class Event(models.Model):

    TIPOS_TERAPIA = [
        ("ABA","Aba"),
        ("CLINICO","Clinico"),
        ("PARTICULAR","Particular"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='paciente')
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.PROTECT, related_name='terapeuta')
    cidade = models.CharField(max_length=12)
    tipo_terapia = models.CharField(max_length=12, choices=TIPOS_TERAPIA, default='')
    guia = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    descricao = models.TextField(null=False, blank=False)
    confirmado = models.BooleanField(default=False)

    # Campo de métrica para contar eventos
    metric_count = models.IntegerField(default=0, editable=False)

    objects = EventManager()

    def get_absolute_url(self):
        return reverse("calendario:event-detail", args=(self.id,))
    
    ##ajusta a condição de tempo para salvar o final trinta minutos depois do inicio da consulta
    def save(self, *args, **kwargs):

        # Incrementa a métrica toda vez que um evento é criado
        if not self.pk:  # Se o evento é novo (não tem chave primária ainda)
            self.metric_count = Event.objects.count() + 1

        if self.start_time and not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=30)


        super(Event, self).save(*args, **kwargs)

    @property
    def get_html_url(self):
        url = reverse("calendario:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.paciente} </a>'

    def __str__(self):
        return f'{self.paciente} - {self.start_time.strftime("%d/%m/%Y %H:%M")}'

class EventMember(EventAbstract):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_members"
    )

    class Meta:
        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)
