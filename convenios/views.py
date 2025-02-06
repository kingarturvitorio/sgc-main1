from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.http import JsonResponse
# Create your views here.

class ConvenioListView(ListView):
    model = models.Convenio
    template_name = 'convenio-list.html'
    context_object_name = 'convenios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class ConvenioCreateView(CreateView):
    model = models.Convenio
    template_name = 'convenio-create.html'
    form_class = forms.ConvenioForm
    success_url = reverse_lazy('convenio-list')

class ConvenioDetailView(DetailView):
    model = models.Convenio
    template_name = 'convenio-detail.html'

class ConvenioUpdateView(UpdateView):
    model = models.Convenio
    template_name = 'convenio-update.html'
    form_class = forms.ConvenioForm
    success_url = reverse_lazy('convenio-list')

class ConvenioDeleteView(DeleteView):
    model = models.Convenio
    template_name = 'convenio-delete.html'
    success_url = reverse_lazy('convenio-list')
