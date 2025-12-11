from django.urls import path
from .views import EventoListAPIView, InscricaoCreateAPIView, InscricaoListAPIView

urlpatterns = [
    path('eventos/', EventoListAPIView.as_view(), name='api_event_list'),
    path('eventos/<int:pk>/inscrever/', InscricaoCreateAPIView.as_view(), name='api_enroll_event'),
    path('minhas-inscricoes/', InscricaoListAPIView.as_view(), name='api_my_inscriptions'),
]