from django import forms
from .models import Evento
from users.models import Usuario
from datetime import date

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = [
            'nome_evento', 
            'apresentador',    
            'tipo_evento', 
            'data',
            'horario_inicio',
            'horario_fim',  
            'local', 
            'qtd_participantes',
            'banner'
        ]
        
        widgets = {
            'nome_evento': forms.TextInput(attrs={'placeholder': 'Ex: Semana da Computação'}),
            'apresentador': forms.TextInput(attrs={'placeholder': 'Ex: Dr. Fulano de Tal'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_evento = cleaned_data.get('data')
        apresentador_nome = cleaned_data.get('apresentador')

        if data_evento and data_evento < date.today():
            self.add_error('data', 'A data do evento não pode ser anterior à data atual.')

        if not apresentador_nome:
            self.add_error('apresentador', 'O campo Apresentador é obrigatório (Professor Responsável).')

        return cleaned_data