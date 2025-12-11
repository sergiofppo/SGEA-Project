from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse

def send_confirmation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Ative sua conta no GoEvents!'
    
    # Gera o UID (ID do usuário criptografado) e o Token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Monta o link de ativação
    link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activate_url = f"http://{current_site.domain}{link}"
    
    message = f"Olá {user.username},\n\nPor favor, clique no link abaixo para ativar sua conta:\n{activate_url}\n\nObrigado!"
    
    email = EmailMessage(
        mail_subject,
        message,
        to=[user.email]
    )
    email.send()