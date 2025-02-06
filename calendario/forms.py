from django.forms import ModelForm, DateInput
from django import forms
from . import models
from datetime import timedelta


class EventForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = ['paciente', 'terapeuta', 'convenio', 'cidade', 
                    'tipo_terapia', 'guia', 'start_time', 'end_time', 'descricao', 'confirmado']
        widgets = {
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'terapeuta': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "descricao": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Observações",
                }
            ),
        }

    ##ajusta a condição de tempo para salvar o final trinta minutos depois do inicio da consulta
    def save(self, commit=True):
        instance = super(EventForm, self).save(commit=False)
        instance.end_time = instance.start_time + timedelta(minutes=30)

        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = models.EventMember
        fields = ["user"]