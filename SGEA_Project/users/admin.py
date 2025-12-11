from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # Importe o seu modelo personalizado

# Registra o seu usuário para aparecer no painel usando o layout padrão de admin
admin.site.register(Usuario, UserAdmin)