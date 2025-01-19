from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from calendario.models import Event
from .models import Terapeuta

@receiver(pre_save, sender=Terapeuta)
def cache_old_terapeuta_name(sender, instance, **kwargs):
    """
    Armazena o nome antigo do terapeuta antes de ele ser salvo.
    """
    if instance.pk:  # Se o terapeuta já existe
        old_instance = Terapeuta.objects.get(pk=instance.pk)
        instance._old_nome_terapeuta = old_instance.nome_terapeuta
    else:
        instance._old_nome_terapeuta = None


@receiver(post_save, sender=Terapeuta)
def update_events_on_terapeuta_save(sender, instance, **kwargs):
    """
    Atualiza eventos associados ao terapeuta salvo, usando o nome antigo para localizar eventos.
    """
    old_nome = getattr(instance, '_old_nome_terapeuta', None)
    new_nome = instance.nome_terapeuta.strip()

    if old_nome:
        eventos_relacionados = Event.objects.filter(terapeuta__iexact=old_nome.strip())
        updated_count = eventos_relacionados.update(terapeuta=new_nome)
        print(f"Signal acionado para terapeuta: {new_nome}")
        print(f"Eventos relacionados encontrados: {eventos_relacionados.count()}")
        for evento in eventos_relacionados:
            print(f"- Evento encontrado: {evento.id} com terapeuta {evento.terapeuta}")
        print(f"Eventos atualizados: {updated_count}")
    else:
        print(f"Novo terapeuta criado: {new_nome} (sem eventos para atualizar)")
