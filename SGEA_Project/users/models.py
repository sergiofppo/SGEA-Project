from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(
        max_length=15, 
        verbose_name='Telefone', 
        blank=True, 
        null=True
    )
    
    instituicao_ensino = models.CharField(
        max_length=100, 
        verbose_name='Instituição de Ensino', 
        blank=True, 
        null=True
    )

    PERFIL_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ORGANIZADOR', 'Organizador'),
    )
    
    perfil = models.CharField(
        max_length=15,
        choices=PERFIL_CHOICES,
        default='ALUNO',
        verbose_name='Perfil'
    )
    
    data_registro = models.DateTimeField(auto_now_add=True)
    
    # Campo para armazenar o token de confirmação de e-mail
    # Deixamos null=True para evitar erros ao criar superusuários via terminal
    email_confirm_token = models.CharField(max_length=100, blank=True, null=True)

    # Sobrescrevemos o is_active para nascer False (inativo) até confirmar o e-mail
    is_active = models.BooleanField(
        default=False, 
        help_text='Indica se o usuário deve ser tratado como ativo. Desmarque isso em vez de excluir contas.', 
        verbose_name='ativo'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username