from django import forms

from . import models

class TerapeutaForm(forms.ModelForm):


    class Meta:
        model = models.Terapeuta
        fields = ['nome_terapeuta', 'email', 'contato', 'titulo_profissional', 
                    'tipo', 'funcao', 'acordo',
                    'valor', 'registro_classe', 'conselho_classe',
                    'dados_bancarios', 'documentos', 'outros']
        widgets = {
            'nome': forms.TextInput({'class':'form-control'}),
            #'email': forms.Textarea({'class':'form-control', 'rows':3}),
        }
        labels = {
            'nome_terapeuta': 'Nome do Terapeuta',
            'email': 'Email',
        }