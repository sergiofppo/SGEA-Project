from rest_framework import serializers
from events.models import Evento, Inscricao
from users.models import Usuario
from django.db import IntegrityError 

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'perfil']

class EventoSerializer(serializers.ModelSerializer):
    organizador_responsavel = UsuarioSerializer(read_only=True)
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id', 'nome_evento', 'apresentador', 'tipo_evento', 'tipo_evento_display',
            'data', 'horario_inicio', 'horario_fim', 'local', 'qtd_participantes',
            'banner', 'organizador_responsavel'
        ]

class InscricaoSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    evento = serializers.PrimaryKeyRelatedField(queryset=Evento.objects.all()) 

    class Meta:
        model = Inscricao
        fields = ['id', 'usuario', 'evento', 'data_inscricao', 'certificado_emitido']
        read_only_fields = ['data_inscricao', 'certificado_emitido']

    def validate(self, data):
        user = self.context['request'].user
        evento = data['evento']

        if Inscricao.objects.filter(usuario=user, evento=evento).exists():
            raise serializers.ValidationError("Você já está inscrito neste evento.")

        if user == evento.organizador_responsavel:
            raise serializers.ValidationError("Organizadores não podem se inscrever em eventos.")
            
        if user.get_full_name() == evento.apresentador:
            raise serializers.ValidationError("Você é o apresentador e não pode se inscrever no próprio evento.")
            
        inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
        if inscritos_atuais >= evento.qtd_participantes:
            raise serializers.ValidationError("Desculpe, este evento está lotado.")
            
        return data