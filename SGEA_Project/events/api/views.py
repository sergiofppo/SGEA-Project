# miguellferraz/sgea-project/SGEA-Project-637ab43d21bdc4fa23b9a804267a9889baf9aab4/SGEA_Project/events/api/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from events.models import Evento, Inscricao
from .serializers import EventoSerializer, InscricaoSerializer
from django.db.models import Count
from django.db.models.functions import Coalesce
from audit.utils import log_action # NOVO IMPORT

class EventoListAPIView(generics.ListAPIView):
    queryset = Evento.objects.all().annotate(
        inscritos_atuais=Coalesce(Count('inscricao'), 0)
    ).order_by('data')
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'events.list' 

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        log_action(
            user=request.user, 
            action_type='EVENT_API_VIEW', 
            details=f"Consulta de lista de eventos via API. Filtros: {request.query_params}"
        )
        return response

class InscricaoCreateAPIView(generics.CreateAPIView):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'events.enroll' 

    def create(self, request, *args, **kwargs):
        try:
            evento = Evento.objects.get(pk=kwargs.get('pk'))
        except Evento.DoesNotExist:
            return Response({"detail": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = {'evento': evento.pk, 'usuario': request.user.pk}
        serializer = self.get_serializer(data=data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        log_action(
            user=request.user, 
            action_type='ENROLL_CREATE', 
            details=f"Inscrição via API no evento '{evento.nome_evento}' (ID: {evento.pk})."
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": f"Inscrição realizada com sucesso no evento: {evento.nome_evento}.", "inscricao": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class InscricaoListAPIView(generics.ListAPIView):
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Inscricao.objects.filter(usuario=self.request.user).order_by('evento__data')