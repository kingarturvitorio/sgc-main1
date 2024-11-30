from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
# Create your views here.

class TerapeutaListView(ListView):
    model = models.Terapeuta
    template_name = 'terapeuta-list.html'
    context_object_name = 'terapeutas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_terapeuta = self.request.GET.get('nome_terapeuta')

        if nome_terapeuta:
            queryset = queryset.filter(nome_terapeuta__icontains=nome_terapeuta)
        return queryset

class TerapeutaCreateView(CreateView):
    model = models.Terapeuta
    template_name = 'terapeuta-create.html'
    form_class = forms.TerapeutaForm
    success_url = reverse_lazy('terapeuta-list')

class TerapeutaDetailView(DetailView):
    model = models.Terapeuta
    template_name = 'terapeuta-detail.html'

class TerapeutaUpdateView(UpdateView):
    model = models.Terapeuta
    template_name = 'terapeuta-update.html'
    form_class = forms.TerapeutaForm
    success_url = reverse_lazy('terapeuta-list')

class TerapeutaDeleteView(DeleteView):
    model = models.Terapeuta
    template_name = 'terapeuta-delete.html'
    success_url = reverse_lazy('terapeuta-list')
