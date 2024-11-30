from django import forms

from . import models

class ProntuarioForm(forms.ModelForm):


    class Meta:
        model = models.Prontuario
        fields = ['event', 'prontuario',]
        
        widgets = {
            'prontuario': forms.Textarea({'class':'form-control', 'rows':20}),
        }
        labels = {
            'event': 'Agendamento',
        }
