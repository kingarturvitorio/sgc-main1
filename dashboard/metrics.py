from calendario.models import Event, Paciente, Terapeuta


def get_product_metrics():
    event = Event.objects.all()
    paciente = Paciente.objects.all()
    terapeuta = Terapeuta.objects.all()

    total_event = sum(even.metric_count for even in event)
    total_pacientes = sum(pacientes.metric_paciente for pacientes in paciente)
    total_terapeutas = sum(terapeutas.metric_terapeuta for terapeutas in terapeuta)

    return dict(
        total_event = total_event,
        total_pacientes = total_pacientes,
        total_terapeutas = total_terapeutas,
    )
