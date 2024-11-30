from django import forms

from . import models

class PacienteForm(forms.ModelForm):


    class Meta:
        model = models.Paciente
        fields = ['nome', 'carteirinha', 'documento', 'endereco', 'telefone_responsavel', 
                    'telefone_contato', 'telefone_emergencia', 'tipo_convenio',
                    'data_nascimento', 'nome_responsavel', 'documento_responsavel',
                    'foto_carteirinha']
        widgets = {
            'nome': forms.TextInput({'class':'form-control'}),
            'documento': forms.Textarea({'class':'form-control', 'rows':3}),
        }
        labels = {
            'nome': 'Nome do Paciente',
            'documento': 'Documento do Paciente',
        }