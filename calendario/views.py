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
from prontuarios.models import Prontuario
import calendar
from django.shortcuts import get_object_or_404
from calendario.utils import Calendar
# Create your views here.
from datetime import timedelta, datetime, date
import pytz

from django.utils.dateparse import parse_datetime


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
        periodo = request.POST.get('tempo')  # Captura o campo 'tempo' (checkbox)

        # Calcula automaticamente o `end_time` (30 minutos após o `start_time`)
        if not start_time:
            return JsonResponse({'error': 'Data inicial inválida'}, status=400)
        

        # Define o tempo de duração baseado no checkbox
        if periodo == "1h":  
            end_time = start_time + timedelta(hours=1)
        else:  
            end_time = start_time + timedelta(minutes=30)  # Padrão

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
        
        # if created:
        #     print(f"Evento criado com ID: {event.id}")
        # else:
        #     print(f"Evento já existente com ID: {event.id}")

        # Lógica para replicar o evento semanalmente por 12 meses
        if replicar:
            for semana in range(1, 53):  # Próximas 52 semanas (12 meses)
                novo_start_time = start_time + timedelta(weeks=semana)
                novo_end_time = novo_start_time + timedelta(hours=1 if periodo == "1h" else 0.5)
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
    if request.method == 'POST':
        terapeuta_nome = request.POST.get('terapeuta_nome')  # Obtendo o terapeuta enviado

        paciente = get_object_or_404(Paciente, id=paciente_id)

        # Filtrar apenas os eventos desse paciente com esse terapeuta
        events = models.Event.objects.filter(paciente=paciente.nome, terapeuta=terapeuta_nome)

        if not events.exists():
            return JsonResponse({'success': False, 'message': 'Nenhum evento encontrado para este paciente e terapeuta.'})

        # Deletando os eventos filtrados
        events_deleted, _ = events.delete()

        return JsonResponse({'success': True, 'message': f'{events_deleted} eventos deletados com sucesso!'})
    
    return JsonResponse({'success': False, 'message': 'Método inválido'})

def delete_future_events(request, paciente_id):
    if request.method == 'POST':
        data_referencia = request.POST.get('start_time')  # Data do evento clicado
        terapeuta_nome = request.POST.get('terapeuta_nome')

        if not data_referencia:
            return JsonResponse({'success': False, 'message': 'Data de referência ausente.'})

        try:
            # Convertendo string ISO para datetime
            data_referencia = parse_datetime(data_referencia)
            if not data_referencia:
                raise ValueError("Data inválida")

            # Filtra eventos daquele paciente a partir da data selecionada
            eventos = models.Event.objects.filter(
                paciente__iexact=Paciente.objects.get(id=paciente_id).nome.strip(),
                start_time__gte=data_referencia
            )

            if terapeuta_nome:
                eventos = eventos.filter(terapeuta__iexact=terapeuta_nome.strip())

            count = eventos.count()
            eventos.delete()

            return JsonResponse({'success': True, 'deleted': count})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

# def confirm_event(request, event_id):
#     if request.method == 'POST':
#         try:
#             event = models.Event.objects.get(id=event_id)
#             # Update the event's confirmation status
#             event.confirmado = True  # Assuming you have a 'confirmed' field in your model
            
#             event.confirmed_color = 'green'
#             event.save()
#             return JsonResponse({
#                 'status': 'success',
#                 'backgroundColor': event.confirmed_color,
#                 'borderColor': event.confirmed_color
#             })
#         except models.Event.DoesNotExist:
#             return JsonResponse({'error': 'Event not found'}, status=404)
#         except Terapeuta.DoesNotExist:
#             return JsonResponse({'error': 'Therapist not found'}, status=404)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
    
def confirm_event(request, event_id):
    if request.method == 'POST':
        try:
            event = models.Event.objects.get(id=event_id)

            # Dados do formulário
            foi_pago = request.POST.get('foi_pago') == 'sim'
            valor_pago = request.POST.get('valor_pago')
            comprovante = request.FILES.get('comprovante')

            event.confirmado = True
            event.confirmed_color = 'green'
            event.foi_pago = foi_pago

            if foi_pago:
                if valor_pago:
                    event.valor_pago = valor_pago
                if comprovante:
                    event.comprovante = comprovante

            event.save()

            return JsonResponse({
                'status': 'success',
                'backgroundColor': event.confirmed_color,
                'foi_pago': event.foi_pago,
                'valor_pago': str(event.valor_pago),
                'comprovante_url': event.comprovante.url if event.comprovante else None,
            })

        except models.Event.DoesNotExist:
            return JsonResponse({'error': 'Evento não encontrado'}, status=404)

    return JsonResponse({'error': 'Requisição inválida'}, status=400)

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

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return JsonResponse({"error": "Parâmetros start_date e end_date são obrigatórios"}, status=400)

    try:
        start_date = parse_datetime(start_date_str)
        end_date = parse_datetime(end_date_str)
        if not start_date or not end_date:
            raise ValueError("Datas inválidas")
    except ValueError:
        return JsonResponse({"error": "Formato de data inválido"}, status=400)

    # Verifica se o usuário pode ver todos os eventos
    user = request.user
    pode_ver_todos = user.is_superuser or user.groups.filter(name__in=['Agendamento', 'Administrativo']).exists()

    # Busca todos os eventos, ou apenas do terapeuta correspondente ao nome do usuário
    if pode_ver_todos:
        events = models.Event.objects.filter(start_time__gte=start_date, end_time__lte=end_date)
    else:
        # Match pelo nome do terapeuta
        nome_usuario = user.get_full_name().split()[0].lower() if user.get_full_name() else user.username.lower()
        events = models.Event.objects.filter(
            start_time__gte=start_date,
            end_time__lte=end_date,
            terapeuta__icontains=nome_usuario
        )

    # Continua o processamento dos eventos como já faz
    events_list = []
    events_dict = {}

    for event in events:
        terapeuta_nome = event.terapeuta
        terapeuta_cor = 'blue'

        try:
            terapeuta = Terapeuta.objects.get(nome_terapeuta=terapeuta_nome)
            terapeuta_cor = terapeuta.cor
        except Terapeuta.DoesNotExist:
            pass

        paciente_nome = event.paciente
        paciente_id = None

        try:
            paciente = Paciente.objects.filter(nome=paciente_nome).first()
            paciente_id = paciente.id if paciente else None
        except Paciente.DoesNotExist:
            pass

        prontuario_id = None
        prontuario = Prontuario.objects.filter(event=event).first()
        if prontuario:
            prontuario_id = prontuario.id

        background_color = event.confirmed_color if event.confirmado else terapeuta_cor

        if event.id not in events_dict:
            events_dict[event.id] = {
                'id': event.id,
                'title': paciente_nome,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'backgroundColor': background_color,
                'extendedProps': {
                    'paciente': paciente_nome,
                    'paciente_id': paciente_id,
                    'terapeuta': str(event.terapeuta),
                    'convenio': event.convenio,
                    'guia': event.guia,
                    'descricao': event.descricao,
                    'prontuario_id': prontuario_id,
                    'foi_pago': event.foi_pago,
                    'valor_pago': str(event.valor_pago) if event.valor_pago else None,
                    'comprovante_url': event.comprovante.url if event.comprovante else None,
                }
            }

    return JsonResponse(list(events_dict.values()), safe=False)



def filter_events(request):
    if request.method == 'GET':
        terapeuta_nome = request.GET.get('terapeuta_nome')  # Nome do terapeuta
        start_date = request.GET.get('start_date')  # Data inicial (recebida do calendário)
        end_date = request.GET.get('end_date')  # Data final (recebida do calendário)

        # ✅ Validação das datas recebidas
        if not start_date or not end_date:
            return JsonResponse({'error': 'As datas de início e fim são obrigatórias'}, status=400)

        try:
            start_date = datetime.fromisoformat(start_date[:10])  # Converter para formato de data
            end_date = datetime.fromisoformat(end_date[:10])  

            # ✅ Filtrar eventos pelo intervalo de tempo correto (Mês, Semana, Dia, Agenda)
            eventos = models.Event.objects.filter(start_time__range=[start_date, end_date])

            # ✅ Filtrar pelo nome do terapeuta, caso informado
            if terapeuta_nome:
                eventos = eventos.filter(terapeuta__icontains=terapeuta_nome)  # 🔹 Correção aqui!

            # Criar dicionário para armazenar os eventos sem duplicatas
            eventos_dict = {}

            for evento in eventos:
                # Buscar cor do terapeuta
                try:
                    terapeuta = Terapeuta.objects.get(nome_terapeuta=evento.terapeuta)
                    terapeuta_cor = terapeuta.cor
                except Terapeuta.DoesNotExist:
                    terapeuta_cor = 'blue'  # Cor padrão se não encontrado

                # Buscar paciente
                paciente_nome = evento.paciente  # Campo paciente (provavelmente um nome)
                paciente_id = None

                try:
                    paciente = Paciente.objects.filter(nome=paciente_nome).first()
                    paciente_id = paciente.id if paciente else None
                except Paciente.DoesNotExist:
                    paciente_id = None

                # Determinar a cor do evento
                background_color = evento.confirmed_color if evento.confirmado else terapeuta_cor

                # Adicionar evento ao dicionário (para evitar duplicatas)
                if evento.id not in eventos_dict:
                    eventos_dict[evento.id] = {
                        'id': evento.id,
                        'title': paciente_nome,  # Nome do paciente no título
                        'start': evento.start_time.isoformat(),
                        'end': evento.end_time.isoformat(),
                        'backgroundColor': background_color,
                        'extendedProps': {
                            'paciente': paciente_nome,
                            'paciente_id': paciente_id,
                            'terapeuta': str(evento.terapeuta),
                            'convenio': evento.convenio,
                            'guia': evento.guia,
                            'descricao': evento.descricao
                        }
                    }

            # ✅ Retornar lista de eventos filtrados
            eventos_list = list(eventos_dict.values())
            print(f"Filtered Events Returned: {len(eventos_list)}")
            
            return JsonResponse(eventos_list, safe=False)

        except ValueError:
            return JsonResponse({'error': 'Datas inválidas'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_terapeutas(request):
    terapeutas = Terapeuta.objects.all().values('id', 'nome_terapeuta')  # Ajuste conforme seu modelo
    return JsonResponse(list(terapeutas), safe=False)
