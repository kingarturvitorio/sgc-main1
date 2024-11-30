from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
# Create your views here.

class PacienteListView(ListView):
    model = models.Paciente
    template_name = 'paciente-list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class PacienteCreateView(CreateView):
    model = models.Paciente
    template_name = 'paciente-create.html'
    form_class = forms.PacienteForm
    success_url = reverse_lazy('paciente-list')

class PacienteDetailView(DetailView):
    model = models.Paciente
    template_name = 'paciente-detail.html'

class PacienteUpdateView(UpdateView):
    model = models.Paciente
    template_name = 'paciente-update.html'
    form_class = forms.PacienteForm
    success_url = reverse_lazy('paciente-list')

class PacienteDeleteView(DeleteView):
    model = models.Paciente
    template_name = 'paciente-delete.html'
    success_url = reverse_lazy('paciente-list')
