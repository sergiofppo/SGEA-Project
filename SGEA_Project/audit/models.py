from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('USER_CREATE', 'Criação de Usuário'),
        ('EVENT_CREATE', 'Cadastro de Evento'),
        ('EVENT_UPDATE', 'Alteração de Evento'),
        ('EVENT_DELETE', 'Exclusão de Evento'),
        ('EVENT_API_VIEW', 'Consulta de Evento via API'),
        ('CERTIFICATE_GENERATE', 'Geração de Certificado'),
        ('CERTIFICATE_VIEW', 'Consulta de Certificado'),
        ('ENROLL_CREATE', 'Inscrição em Evento'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Usuário Responsável'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name='Ação')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')
    details = models.TextField(blank=True, null=True, verbose_name='Detalhes da Ação')

    class Meta:
        verbose_name = 'Registro de Auditoria'
        verbose_name_plural = 'Registros de Auditoria'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"