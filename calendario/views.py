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
from terapeutas.models import Terapeuta
from pacientes.models import Paciente
import calendar
from django.shortcuts import get_object_or_404
from calendario.utils import Calendar
# Create your views here.
from datetime import timedelta, datetime, date
import pytz

import logging

logger = logging.getLogger(__name__)

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
                    "convenio": event.convenio,
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
        convenio = form.cleaned_data["convenio"]
        cidade = form.cleaned_data["cidade"]
        tipo_terapia = form.cleaned_data["tipo_terapia"]
        guia = form.cleaned_data["guia"]
        start_time = form.cleaned_data["start_time"]
        descricao = form.cleaned_data["descricao"]
        replicar = request.POST.get('replicar') == 'on'  # Captura o estado do checkbox

        # Calcula automaticamente o `end_time` (30 minutos após o `start_time`)
        if not start_time:
            return JsonResponse({'error': 'Data inicial inválida'}, status=400)
        end_time = start_time + timedelta(minutes=30)

        # Busca a cor do terapeuta
        try:
            terapeuta_obj = Terapeuta.objects.get(nome_terapeuta=terapeuta)
            terapeuta_cor = terapeuta_obj.cor
        except Terapeuta.DoesNotExist:
            terapeuta_cor = 'blue'  # Cor padrão caso não encontre o terapeuta

        # Cria o evento no banco de dados
        event, created = models.Event.objects.get_or_create(
            paciente=paciente,
            terapeuta=terapeuta,
            convenio=convenio,
            cidade=cidade,
            tipo_terapia=tipo_terapia,
            guia=guia,
            start_time=start_time,
            end_time=end_time,
            descricao=descricao,
        )
        
        if created:
            print(f"Evento criado com ID: {event.id}")
        else:
            print(f"Evento já existente com ID: {event.id}")

        # Lógica para replicar o evento semanalmente por 12 meses
        if replicar:
            for semana in range(1, 53):  # Próximas 52 semanas (12 meses)
                novo_start_time = start_time + timedelta(weeks=semana)
                novo_end_time = novo_start_time + timedelta(minutes=30)
                models.Event.objects.create(
                    paciente=paciente,
                    terapeuta=terapeuta,
                    convenio=convenio,
                    cidade=cidade,
                    tipo_terapia=tipo_terapia,
                    guia=guia,
                    start_time=novo_start_time,
                    end_time=novo_end_time,
                    descricao=descricao,
                )
                print(f"Evento replicado para: {novo_start_time}")
        # Serializa os dados para JSON, incluindo a cor do terapeuta
        return JsonResponse({
            'id': event.id,
            'title': str(paciente),
            'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'backgroundColor': terapeuta_cor,
            'borderColor': terapeuta_cor,
            'paciente': str(paciente),
            'terapeuta': str(terapeuta),
            'convenio': str(convenio),
            'cidade': str(cidade),
            'guia': str(guia),
            'descricao': descricao,
        })

    # Caso não seja POST ou form inválido
    return JsonResponse({'error': 'Dados inválidos'}, status=400)



def delete_event(request, event_id):
    event = get_object_or_404(models.Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def delete_all_events(request, paciente_id):
    # Verifica se o paciente existe
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Deleta todos os eventos associados a este paciente
    events_deleted, _ = models.Event.objects.filter(paciente=paciente).delete()

    if events_deleted > 0:
        return JsonResponse({'success': True, 'message': f'{events_deleted} eventos deletados com sucesso!'})
    else:
        return JsonResponse({'success': False, 'message': 'Nenhum evento encontrado para este paciente.'})

def confirm_event(request, event_id):
    if request.method == 'POST':
        try:
            event = models.Event.objects.get(id=event_id)
            # Update the event's confirmation status
            event.confirmado = True  # Assuming you have a 'confirmed' field in your model
            
            event.confirmed_color = 'green'
            event.save()
            return JsonResponse({
                'status': 'success',
                'backgroundColor': event.confirmed_color,
                'borderColor': event.confirmed_color
            })
        except models.Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Terapeuta.DoesNotExist:
            return JsonResponse({'error': 'Therapist not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)
    

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

    events_dict = {}  # Usaremos um dicionário para garantir unicidade

    for event in events:
    
        # Busca o terapeuta relacionado com base em algum atributo no evento
        terapeuta_nome = event.terapeuta  # Ajuste conforme seu modelo
        terapeuta_cor = None

        # Tenta buscar a cor do terapeuta pelo nome
        try:
            terapeuta = Terapeuta.objects.get(nome_terapeuta=terapeuta_nome)
            terapeuta_cor = terapeuta.cor
        except Terapeuta.DoesNotExist:
            terapeuta_cor = 'blue'  # Cor padrão caso não encontre

        # Se o paciente for armazenado como uma string (nome)
        paciente_nome = event.paciente  # Aqui estamos pegando o nome do paciente do evento
        paciente_id = None  # Já que não é uma ForeignKey, não há um ID relacionado diretamente

        # Caso o paciente tenha sido criado e você queira associar um paciente pelo nome
        try:
            paciente = Paciente.objects.get(nome=paciente_nome)  # Supondo que você tem um campo nome
            paciente_id = paciente.id  # Agora que temos o paciente, podemos pegar o ID dele
        except Paciente.DoesNotExist:
            paciente_id = None  # Caso o paciente não exista, deixamos como None ou algum valor padrão

        # Use the confirmed color if the event is confirmed
        background_color = event.confirmed_color if event.confirmado else terapeuta_cor

        # Adiciona o evento ao dicionário, garantindo unicidade pelo ID
        if event.id not in events_dict:
            events_dict[event.id] = {
                'id': event.id,
                'title': paciente_nome,  # Nome do paciente como título
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'backgroundColor': background_color,
                'extendedProps': {
                    'paciente': paciente_nome,
                    'paciente_id': paciente_id,
                    'terapeuta': str(event.terapeuta),
                    'convenio': event.convenio,
                    'guia': event.guia,
                    'descricao': event.descricao
                }
            }

    # Converte os valores do dicionário em uma lista para o JSON
    events_list = list(events_dict.values())
    
    print(f"Eventos retornados: {len(events_list)}")
    
    return JsonResponse(events_list, safe=False)


def filter_events(request):
    if request.method == 'GET':
        terapeuta_nome = request.GET.get('terapeuta_nome')  # Get the therapist name from the request

        # Filter events by the therapist's name
        events = models.Event.objects.filter(terapeuta=terapeuta_nome)  # Adjust according to your model

        events_dict = {}  # Use a dictionary to ensure uniqueness

        for event in events:
            # Fetch the therapist's color based on the event's therapist name
            terapeuta_cor = None
            try:
                terapeuta = Terapeuta.objects.get(nome_terapeuta=terapeuta_nome)
                terapeuta_cor = terapeuta.cor
            except Terapeuta.DoesNotExist:
                terapeuta_cor = 'blue'  # Default color if not found

            # Get the patient name and ID
            paciente_nome = event.paciente  # Assuming this is a string
            paciente_id = None  # No direct ID since it's not a ForeignKey

            try:
                paciente = Paciente.objects.get(nome=paciente_nome)  # Assuming you have a field for the name
                paciente_id = paciente.id  # Get the patient's ID
            except Paciente.DoesNotExist:
                paciente_id = None  # If the patient does not exist

            # Use the confirmed color if the event is confirmed
            background_color = event.confirmed_color if event.confirmado else terapeuta_cor

            # Add the event to the dictionary, ensuring uniqueness by ID
            if event.id not in events_dict:
                events_dict[event.id] = {
                    'id': event.id,
                    'title': paciente_nome,  # Patient's name as title
                    'start': event.start_time.isoformat(),
                    'end': event.end_time.isoformat(),
                    'backgroundColor': background_color,
                    'extendedProps': {
                        'paciente': paciente_nome,
                        'paciente_id': paciente_id,
                        'terapeuta': str(event.terapeuta),
                        'convenio': event.convenio,
                        'guia': event.guia,
                        'descricao': event.descricao
                    }
                }

        # Convert the dictionary values to a list for JSON
        events_list = list(events_dict.values())
        
        print(f"Filtered Events Returned: {len(events_list)}")
        
        return JsonResponse(events_list, safe=False)  # Return the data as JSON

    return JsonResponse({'error': 'Invalid request'}, status=400)

