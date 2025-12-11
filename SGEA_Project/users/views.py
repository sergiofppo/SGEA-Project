from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import Usuario
from audit.utils import log_action 
from .utils import send_confirmation_email
from django.contrib import messages

class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.object.email:
            send_confirmation_email(self.object, self.request)
        
        log_action(
            user=self.object, 
            action_type='USER_CREATE', 
            details=f"Usuário {self.object.username} ({self.object.perfil}) criado, aguardando confirmação por e-mail."
        )
        
        messages.info(self.request, "Seu cadastro foi realizado com sucesso! Verifique seu e-mail para ativar sua conta.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastro de Novo Usuário'
        return context

def activate_account(request, token):
    try:
        user = Usuario.objects.get(email_confirm_token=token)
    except Usuario.DoesNotExist:
        messages.error(request, "Token de ativação inválido ou expirado.")
        return redirect('login') 

    if user.is_active:
        messages.warning(request, "Esta conta já estava ativa. Faça login para continuar.")
        return redirect('login')
        
    user.is_active = True
    user.save()
    
    messages.success(request, "Conta ativada com sucesso! Você já pode fazer login.")
    
    log_action(
        user=user, 
        action_type='USER_UPDATE', 
        details=f"Usuário {user.username} ativou a conta via link de e-mail."
    )
    
    return redirect('login')