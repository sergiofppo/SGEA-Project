from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
import re

class CustomUserCreationForm(UserCreationForm):
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
            'username': 'Nome de Usuário (Login)',
            'email': 'E-mail (Opcional)',
            'first_name': 'Nome Completo',
        }

    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get("perfil")
        instituicao = cleaned_data.get("instituicao_ensino")
        telefone = cleaned_data.get("telefone")

        if perfil in ['ALUNO', 'PROFESSOR'] and not instituicao:
            self.add_error('instituicao_ensino', 'Este campo é obrigatório para perfis de Aluno ou Professor.')

        if telefone:
            phone_pattern = re.compile(r'^\(\d{2}\) \d{5}-\d{4}$')
            if not phone_pattern.match(telefone):
                self.add_error('telefone', 'Formato de telefone inválido. Use (XX) XXXXX-XXXX.')
        
        return cleaned_data
