from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsuarioRegisterView, activate_account

urlpatterns = [
    # Cadastro
    path('cadastro/', UsuarioRegisterView.as_view(), name='register'),
    
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        next_page='/eventos/'  # Redireciona para a lista de eventos após logar
    ), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/' # Redireciona para a home (landing page) após sair
    ), name='logout'),

    # Ativação de Conta (CORRIGIDO)
    # A view 'activate_account' agora espera dois argumentos (uidb64 e token),
    # então a URL precisa capturar ambos. O nome deve ser 'activate' para bater com o utils.py.
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
]