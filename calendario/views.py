from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms 
import calendar
from django.shortcuts import get_object_or_404
from calendario.utils import Calendar
# Create your views here.
from datetime import timedelta, datetime, date
import pytz

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

class CalendarView(ListView):
    model = models.Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context

class ConsultaCreateView(View):
    template_name = "calendar.html"
    form_class = forms.EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = models.Event.objects.all()
        event_list = []
        
        localtz = pytz.timezone('America/Sao_Paulo')

        for event in events:
            event_list.append(
                {   "id": event.id,
                    "paciente": event.paciente,
                    "terapeuta": event.terapeuta,
                    "cidade": event.cidade,
                    "tipo_terapia": event.tipo_terapia,
                    "guia": event.guia,
                    "start_time": event.start_time.astimezone(localtz).strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_time": event.end_time.astimezone(localtz).strftime("%Y-%m-%dT%H:%M:%S"),
                    "descricao": event.descricao,
                    "confirmado": event.confirmado,
                }
            )
        context = {"form": forms, "events": event_list}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendario:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)

class EventEdit(UpdateView):
    model = models.Event
    fields = ['paciente', 'terapeuta', 'cidade', 
                    'tipo_terapia', 'guia', 'start_time', 'end_time', 'descricao']
    template_name = "event.html"


def create_event(request):
    form = forms.EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        paciente = form.cleaned_data["paciente"]
        terapeuta = form.cleaned_data["terapeuta"]
        cidade = form.cleaned_data["cidade"]
        tipo_terapia = form.cleaned_data["tipo_terapia"]
        guia = form.cleaned_data["guia"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        descricao = form.cleaned_data["descricao"]
        
        # Cria o evento no banco de dados
        event, created = models.Event.objects.get_or_create(
            paciente=paciente,
            terapeuta=terapeuta,
            cidade=cidade,
            tipo_terapia=tipo_terapia,
            guia=guia,
            start_time=start_time,
            end_time=end_time,
            descricao=descricao,
        )
        
        # Serializa os dados para JSON
        return JsonResponse({
            'id': event.id,
            'title': str(paciente),  # Pode usar `str()` para converter para string
            'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'backgroundColor': 'blue',  # ou outra cor padrão
            'borderColor': 'blue',
            'paciente': str(paciente),  # Serializa o nome ou outro atributo
            'terapeuta': str(terapeuta),  # Serializa o nome ou outro atributo
            'guia': str(guia),  # Serializa o nome ou outro atributo
            'descricao': descricao
        })
    
    return render(request, "event.html", {"form": form})



def delete_event(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def confirm_event(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)
    if request.method == 'POST':
        event.confirmado = True  # Supondo que você tenha um campo booleano 'confirmado' no modelo Event
        event.save()
        return JsonResponse({'message': 'Event cofirmado com sucesso.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
    

def next_week(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(models.Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
    

def get_events(request):
    events = models.Event.objects.all()
    events_list = []

    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.paciente.nome,  # Adapte conforme o campo do seu modelo
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'backgroundColor': 'green' if event.confirmado else 'blue',
            'borderColor': 'green' if event.confirmado else 'blue',
            'extendedProps': {
                'paciente': event.paciente.nome,   # Pegando apenas o nome do paciente
                'terapeuta': str(event.terapeuta.nome_terapeuta),  # Pegando o nome do terapeuta
                'guia': event.guia,
                'descricao': event.descricao
            }
        })
    
    return JsonResponse(events_list, safe=False)