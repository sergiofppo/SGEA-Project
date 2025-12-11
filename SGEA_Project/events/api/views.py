from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.db.models import Count
from django.db.models.functions import Coalesce

# Imports do seu projeto
from events.models import Evento, Inscricao
# Importa do arquivo .serializers (que está na mesma pasta 'api')
from .serializers import EventoSerializer, InscricaoSerializer
from audit.utils import log_action

class EventoListAPIView(generics.ListAPIView):
    """
    Lista todos os eventos, incluindo a contagem de inscritos.
    """
    queryset = Evento.objects.all().annotate(
        inscritos_atuais=Coalesce(Count('inscricao'), 0)
    ).order_by('data')
    
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'events.list' 

    def list(self, request, *args, **kwargs):
        # Executa a listagem padrão
        response = super().list(request, *args, **kwargs)
        
        # Registra no log de auditoria
        log_action(
            user=request.user, 
            action_type='EVENT_API_VIEW', 
            details=f"Consulta de lista de eventos via API. Filtros: {request.query_params}"
        )
        return response

class InscricaoCreateAPIView(generics.CreateAPIView):
    """
    Realiza a inscrição do usuário logado em um evento específico.
    """
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'events.enroll' 

    def create(self, request, *args, **kwargs):
        # 1. Verifica se o evento existe antes de tentar serializar
        try:
            evento = Evento.objects.get(pk=kwargs.get('pk'))
        except Evento.DoesNotExist:
            return Response(
                {"detail": "Evento não encontrado."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Prepara os dados
        # O campo 'usuario' é preenchido automaticamente pelo Serializer (HiddenField + CurrentUserDefault)
        # Passamos apenas o evento.
        data = {'evento': evento.pk}
        
        # O context={'request': request} é essencial para o CurrentUserDefault funcionar
        serializer = self.get_serializer(data=data, context={'request': request})

        # 3. Valida (executa as regras do serializers.py: lotação, duplicidade, etc)
        serializer.is_valid(raise_exception=True)

        # 4. Salva a inscrição
        self.perform_create(serializer)

        # 5. Log de Auditoria
        log_action(
            user=request.user, 
            action_type='ENROLL_CREATE', 
            details=f"Inscrição via API no evento '{evento.nome_evento}' (ID: {evento.pk})."
        )
        
        # 6. Retorno personalizado
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "detail": f"Inscrição realizada com sucesso no evento: {evento.nome_evento}.", 
                "inscricao": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class InscricaoListAPIView(generics.ListAPIView):
    """
    Lista apenas as inscrições do usuário logado.
    """
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra para retornar apenas inscrições do usuário atual
        return Inscricao.objects.filter(usuario=self.request.user).order_by('evento__data')