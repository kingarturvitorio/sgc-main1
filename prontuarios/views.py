from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from . import models, forms
# Create your views here.

class ProntuarioListView(ListView):
    model = models.Prontuario
    template_name = 'prontuario-list.html'
    context_object_name = 'prontuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        paciente_id = self.request.GET.get('paciente_id')

        if paciente_id:
            from pacientes.models import Paciente
            try:
                paciente = Paciente.objects.get(id=paciente_id)
                queryset = queryset.filter(event__paciente__icontains=paciente.nome)
            except Paciente.DoesNotExist:
                queryset = queryset.none()

        if nome:
            queryset = queryset.filter(event__paciente__icontains=nome)

        return queryset

class ProntuarioCreateView(CreateView):
    model = models.Prontuario
    template_name = 'prontuario-create.html'
    form_class = forms.ProntuarioForm
    success_url = reverse_lazy('calendario:calendar')

    def get_initial(self):
        initial = super().get_initial()
        event_id = self.request.GET.get('event_id')
        if event_id:
            initial['event'] = event_id
        return initial

class ProntuarioDetailView(DetailView):
    model = models.Prontuario
    template_name = 'prontuario-detail.html'

    context_object_name = 'prontuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prontuario_atual = self.get_object()
        paciente = prontuario_atual.event.paciente

        # Busca todos os outros prontuários do mesmo paciente (excluindo o atual)
        outros_prontuarios = models.Prontuario.objects.filter(
            event__paciente=paciente
        ).exclude(id=prontuario_atual.id).select_related('event').order_by('-event__start_time')

        context['outros_prontuarios'] = outros_prontuarios
        return context

class ProntuarioUpdateView(UpdateView):
    model = models.Prontuario
    template_name = 'prontuario-update.html'
    form_class = forms.ProntuarioForm
    success_url = reverse_lazy('prontuario-list')

class ProntuarioDeleteView(DeleteView):
    model = models.Prontuario
    template_name = 'prontuario-delete.html'
    success_url = reverse_lazy('prontuario-list')

def verificar_prontuarios_paciente(request):
    paciente_id = request.GET.get('paciente_id')

    if not paciente_id:
        return JsonResponse({'error': 'ID do paciente não enviado.'}, status=400)

    try:
        paciente = models.Paciente.objects.get(id=paciente_id)
    except models.Paciente.DoesNotExist:
        return JsonResponse({'error': 'Paciente não encontrado.'}, status=404)

    # Busca por nome (exato ou icontains, dependendo de como está salvo)
    prontuario_existe = models.Prontuario.objects.filter(event__paciente__icontains=paciente.nome).exists()

    return JsonResponse({'tem_prontuario': prontuario_existe})