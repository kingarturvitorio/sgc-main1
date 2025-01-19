from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from calendario.models import Event
from .models import Convenio

@receiver(pre_save, sender=Convenio)
def cache_old_Convenio_name(sender, instance, **kwargs):
    """
    Armazena o nome antigo do Convenio antes de ele ser salvo.
    """
    if instance.pk:  # Se o Convenio já existe
        old_instance = Convenio.objects.get(pk=instance.pk)
        instance._old_nome_convenio = old_instance.nome_convenio
    else:
        instance._old_nome_convenio = None


@receiver(post_save, sender=Convenio)
def update_events_on_Convenio_save(sender, instance, **kwargs):
    """
    Atualiza eventos associados ao Convenio salvo, usando o nome antigo para localizar eventos.
    """
    old_nome = getattr(instance, '_old_nome_convenio', None)
    new_nome = instance.nome_convenio.strip()

    if old_nome:
        eventos_relacionados = Event.objects.filter(convenio__iexact=old_nome.strip())
        updated_count = eventos_relacionados.update(convenio=new_nome)
        print(f"Signal acionado para Convenio: {new_nome}")
        print(f"Eventos relacionados encontrados: {eventos_relacionados.count()}")
        for evento in eventos_relacionados:
            print(f"- Evento encontrado: {evento.id} com Convenio {evento.convenio}")
        print(f"Eventos atualizados: {updated_count}")
    else:
        print(f"Novo Convenio criado: {new_nome} (sem eventos para atualizar)")
