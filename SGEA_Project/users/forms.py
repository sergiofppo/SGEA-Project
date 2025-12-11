from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
import re

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome Completo', 
        max_length=150, 
        required=True
    )

    class Meta:
        model = Usuario
        fields = (
            'username', 
            'email', 
            'first_name', 
            'telefone', 
            'instituicao_ensino', 
            'perfil'
        )
        labels = {
            'username': 'Usuário (Login)',
            'email': 'E-mail',
            'first_name': 'Nome Completo',
            'telefone': 'Celular / WhatsApp',
            'instituicao_ensino': 'Instituição',
            'perfil': 'Eu sou:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ESTILO AUTOMÁTICO: Adiciona classes do Tailwind em todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200'
            field.widget.attrs['placeholder'] = f'Digite seu {field.label.lower()}...'

    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get("perfil")
        instituicao = cleaned_data.get("instituicao_ensino")
        telefone = cleaned_data.get("telefone")

        if perfil in ['ALUNO', 'PROFESSOR'] and not instituicao:
            self.add_error('instituicao_ensino', 'Obrigatório informar a instituição.')

        if telefone:
            phone_pattern = re.compile(r'^\(\d{2}\) \d{5}-\d{4}$')
            if not phone_pattern.match(telefone):
                self.add_error('telefone', 'Use o formato (XX) XXXXX-XXXX')
        
        return cleaned_data