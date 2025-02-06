from django import forms

from . import models

class ConvenioForm(forms.ModelForm):


    class Meta:
        model = models.Convenio
        fields = ['nome_convenio', 'numero_convenio', 'informacoes']
