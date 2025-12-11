from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import get_user_model, login

# Importações para decodificar o token (mantidas para uso futuro)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from .forms import CustomUserCreationForm
from .models import Usuario
from .utils import send_confirmation_email

# Se você ainda não tem o app 'audit', mantenha comentado para não dar erro
# from audit.utils import log_action 

User = get_user_model()

class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # 1. Salva o objeto na memória
        self.object = form.save(commit=False)
        
        # --- MUDANÇA PARA DESENVOLVIMENTO: Ativa direto ---
        self.object.is_active = True  # O usuário já nasce ATIVO
        self.object.save() 

        # 2. Comentamos o envio de e-mail para não dar erro agora
        # if self.object.email:
        #     send_confirmation_email(self.object, self.request)
        #     messages.info(self.request, f"Cadastro realizado! Um link de ativação foi enviado para {self.object.email}.")
        
        # 3. Mensagem de sucesso direta
        messages.success(self.request, "Cadastro realizado com sucesso! Faça seu login.")

        # Log de auditoria (Descomente se tiver o app audit)
        # log_action(
        #     user=self.object,
        #     action_type='USER_CREATE',
        #     details=f"Usuário {self.object.username} ({self.object.perfil}) criado."
        # )
        
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastro de Novo Usuário'
        return context

# Mantemos a função aqui para quando você for reativar o sistema de e-mail no futuro
def activate_account(request, uidb64, token):
    try:
        # Decodifica o ID do usuário
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verifica se o usuário existe e se o token é válido
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Sua conta foi ativada com sucesso! Faça o login.")
        
        # log_action(
        #    user=user,
        #    action_type='USER_UPDATE',
        #    details=f"Usuário {user.username} ativou a conta via e-mail."
        # )
        return redirect('login')
    else:
        messages.error(request, "O link de ativação é inválido ou expirou!")
        return redirect('login')