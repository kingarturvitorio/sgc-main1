from django import forms

from . import models

import random

def gerar_cor_aleatoria():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class TerapeutaForm(forms.ModelForm):


    class Meta:
        model = models.Terapeuta
        fields = ['nome_terapeuta', 'email', 'contato', 'titulo_profissional', 
                    'tipo', 'funcao', 'acordo',
                    'valor', 'registro_classe', 'conselho_classe',
                    'dados_bancarios', 'documentos', 'outros', 'cor']
        widgets = {
            'nome': forms.TextInput({'class':'form-control'}),
            #'email': forms.Textarea({'class':'form-control', 'rows':3}),
        }
        labels = {
            'nome_terapeuta': 'Nome do Terapeuta',
            'email': 'Email',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Adiciona uma cor aleatória ao terapeuta se o campo cor estiver vazio
        if not instance.cor or instance.cor == "#FFFFFF":
            instance.cor = gerar_cor_aleatoria()
        if commit:
            instance.save()
        return instance