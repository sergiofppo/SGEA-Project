from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

def send_confirmation_email(user, request):
    subject = 'GoEvents! - Confirmação de Cadastro'
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'token': str(user.email_confirm_token)})
    )
    
    context = {
        'user': user,
        'activation_link': activation_link,
        'domain': request.get_host(),
        'protocol': request.scheme,
    }
    
    html_content = render_to_string('users/email/activation_email.html', context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar email para {user.email}: {e}")
        return False