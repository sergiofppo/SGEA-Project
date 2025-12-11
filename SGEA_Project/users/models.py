from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15, verbose_name='Telefone', blank=True, null=True)
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
    email_confirm_token = models.CharField(max_length=100, default=uuid.uuid4)

    is_active = models.BooleanField(
        default=False, 
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', 
        verbose_name='active'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username