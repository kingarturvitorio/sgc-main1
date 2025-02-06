from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from calendario.models import Event
from .models import Paciente

@receiver(pre_save, sender=Paciente)
def cache_old_paciente_name(sender, instance, **kwargs):
    """
    Armazena o nome antigo do paciente antes de ele ser salvo.
    """
    if instance.pk:  # Se o paciente já existe
        old_instance = Paciente.objects.get(pk=instance.pk)
        instance._old_nome_paciente = old_instance.nome
    else:
        instance._old_nome_paciente = None


@receiver(post_save, sender=Paciente)
def update_events_on_paciente_save(sender, instance, **kwargs):
    """
    Atualiza eventos associados ao paciente salvo, usando o nome antigo para localizar eventos.
    """
    old_nome = getattr(instance, '_old_nome_paciente', None)
    new_nome = instance.nome.strip()

    if old_nome:
        eventos_relacionados = Event.objects.filter(paciente__iexact=old_nome.strip())
        updated_count = eventos_relacionados.update(paciente=new_nome)
        print(f"Signal acionado para paciente: {new_nome}")
        print(f"Eventos relacionados encontrados: {eventos_relacionados.count()}")
        for evento in eventos_relacionados:
            print(f"- Evento encontrado: {evento.id} com paciente {evento.paciente}")
        print(f"Eventos atualizados: {updated_count}")
    else:
        print(f"Novo paciente criado: {new_nome} (sem eventos para atualizar)")
