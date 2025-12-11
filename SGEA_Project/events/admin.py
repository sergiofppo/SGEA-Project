from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Evento, Inscricao

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome_evento', 'data', 'horario_inicio', 'local', 'qtd_participantes')
    search_fields = ('nome_evento', 'local', 'apresentador')
    list_filter = ('tipo_evento', 'data')

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'data_inscricao', 'certificado_emitido')
    list_filter = ('certificado_emitido', 'data_inscricao')
    search_fields = ('usuario__username', 'evento__nome_evento')
