from django.urls import path
from events.api.views import (
    EventoListAPIView, 
    InscricaoCreateAPIView, 
    InscricaoListAPIView
)

urlpatterns = [
    path('', EventoListAPIView.as_view(), name='api_event_list'), 
    path('<int:pk>/inscrever/', InscricaoCreateAPIView.as_view(), name='api_enroll_event'),
    path('minhas-inscricoes/', InscricaoListAPIView.as_view(), name='api_my_inscriptions'),
]