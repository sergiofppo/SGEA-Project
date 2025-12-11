from rest_framework import serializers
from events.models import Evento, Inscricao
from users.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir dados básicos do usuário (ex: Organizador).
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'perfil']

class EventoSerializer(serializers.ModelSerializer):
    # Nested Serializer: Traz os dados do objeto Usuario ao invés de só o ID
    organizador_responsavel = UsuarioSerializer(read_only=True)
    
    # Campo calculado para mostrar o texto legível do tipo (ex: 'Workshop' ao invés de 'W')
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id', 
            'nome_evento', 
            'apresentador', 
            'tipo_evento', 
            'tipo_evento_display',
            'data', 
            'horario_inicio', 
            'horario_fim', 
            'local', 
            'qtd_participantes',
            'banner', 
            'organizador_responsavel'
        ]

class InscricaoSerializer(serializers.ModelSerializer):
    # HiddenField injeta o usuário logado automaticamente no create
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    
    # PrimaryKeyRelatedField permite selecionar o evento pelo ID na hora de enviar o JSON
    evento = serializers.PrimaryKeyRelatedField(queryset=Evento.objects.all()) 

    class Meta:
        model = Inscricao
        fields = ['id', 'usuario', 'evento', 'data_inscricao', 'certificado_emitido']
        read_only_fields = ['data_inscricao', 'certificado_emitido']

    def validate(self, data):
        """
        Validações personalizadas de negócio.
        """
        user = self.context['request'].user
        evento = data['evento']

        # 1. Verifica se já está inscrito
        if Inscricao.objects.filter(usuario=user, evento=evento).exists():
            raise serializers.ValidationError("Você já está inscrito neste evento.")

        # 2. Organizador não pode se inscrever no próprio evento
        if user == evento.organizador_responsavel:
            raise serializers.ValidationError("Organizadores não podem se inscrever em seus próprios eventos.")
            
        # 3. Apresentador não pode se inscrever (Comparação por nome string)
        # Nota: O uso de .strip() ajuda a evitar erros com espaços em branco acidentais
        apresentador_nome = evento.apresentador.strip().lower() if evento.apresentador else ""
        user_nome = user.get_full_name().strip().lower()
        
        if user_nome and user_nome == apresentador_nome:
            raise serializers.ValidationError("Você é o apresentador e não pode se inscrever no próprio evento.")
            
        # 4. Verifica lotação
        inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
        if inscritos_atuais >= evento.qtd_participantes:
            raise serializers.ValidationError("Desculpe, este evento está lotado.")
            
        return data

    def to_representation(self, instance):
        """
        Personaliza a resposta (Leitura).
        Ao invés de mostrar só o ID do evento, mostra os dados do Evento quando listamos as inscrições.
        """
        representation = super().to_representation(instance)
        # Substitui o ID do evento pelo objeto serializado completo (ou parcial)
        representation['evento'] = EventoSerializer(instance.evento).data
        return representation