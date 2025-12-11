from django.urls import path
# Importamos as views da API da pasta onde você criou (events/api/views.py)
from events.api.views import (
    EventoListAPIView, 
    InscricaoCreateAPIView, 
    InscricaoListAPIView
)

# Se você tiver views HTML normais (para o site), importe-as de events/views.py
# from events.views import EventoListView, EventoDetailView 

urlpatterns = [
    # --- ROTAS DA API (JSON) ---
    # URLs acessíveis em: /eventos/api/...
    
    path('api/eventos/', EventoListAPIView.as_view(), name='api_event_list'),
    
    path('api/eventos/<int:pk>/inscrever/', InscricaoCreateAPIView.as_view(), name='api_enroll_event'),
    
    path('api/minhas-inscricoes/', InscricaoListAPIView.as_view(), name='api_my_inscriptions'),


    # --- ROTAS DO SITE (HTML) ---
    # Aqui ficam as rotas para o navegador (páginas bonitas)
    # IMPORTANTE: Como seu LOGIN_REDIRECT_URL é '/eventos/', você precisa desta rota abaixo:
    
    # path('', EventoListView.as_view(), name='event_list'),  <-- Descomente quando criar a view HTML
]