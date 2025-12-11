from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('criar/', views.EventCreateView.as_view(), name='event_create'),
    path('meus-eventos/', views.MyEventListView.as_view(), name='my_event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/editar/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/excluir/', views.delete_event, name='event_delete'),
    path('<int:pk>/inscrever/', views.enroll_event, name='enroll_event'),
    path('minhas-inscricoes/', views.MyInscriptionsListView.as_view(), name='my_inscriptions'),
    path('inscricao/<int:inscricao_id>/emitir_certificado/', views.emitir_certificado, name='emitir_certificado'),
    path('inscricao/<int:inscricao_id>/certificado/', views.generate_certificate_pdf, name='generate_certificate'),
]