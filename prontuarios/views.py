from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
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

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class ProntuarioCreateView(CreateView):
    model = models.Prontuario
    template_name = 'prontuario-create.html'
    form_class = forms.ProntuarioForm
    success_url = reverse_lazy('prontuario-list')

class ProntuarioDetailView(DetailView):
    model = models.Prontuario
    template_name = 'prontuario-detail.html'

class ProntuarioUpdateView(UpdateView):
    model = models.Prontuario
    template_name = 'prontuario-update.html'
    form_class = forms.ProntuarioForm
    success_url = reverse_lazy('prontuario-list')

class ProntuarioDeleteView(DeleteView):
    model = models.Prontuario
    template_name = 'prontuario-delete.html'
    success_url = reverse_lazy('prontuario-list')