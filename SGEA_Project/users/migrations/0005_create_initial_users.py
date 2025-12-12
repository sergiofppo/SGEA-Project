from django.db import migrations
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

def create_users(apps, schema_editor):
    # Pega o modelo de usuário personalizado
    User = get_user_model()
    
    users_to_create = [
        # Usuário Organizador [cite: 14]
        {
            'username': 'organizador@sgea.com', 
            'password': 'Admin@123', # [cite: 16]
            'email': 'organizador@sgea.com', 
            'first_name': 'Organizador Mestre',
            'perfil': 'ORGANIZADOR',
            'is_staff': True, # Pode acessar o Admin
            'is_superuser': False,
            'is_active': True, # Ativo para login imediato
        },
        # Usuário Aluno [cite: 17]
        {
            'username': 'aluno@sgea.com', 
            'password': 'Aluno@123', # [cite: 19]
            'email': 'aluno@sgea.com', 
            'first_name': 'Aluno Teste',
            'perfil': 'ALUNO',
            'is_active': True,
            'instituicao_ensino': 'Universidade Teste',
        },
        # Usuário Professor [cite: 20]
        {
            'username': 'professor@sgea.com', 
            'password': 'Professor@123', # [cite: 23]
            'email': 'professor@sgea.com', 
            'first_name': 'Professor Teste',
            'perfil': 'PROFESSOR',
            'is_active': True,
            'instituicao_ensino': 'Universidade Teste',
        },
    ]

    for user_data in users_to_create:
        # Pega a senha para gerar o hash
        password = user_data.pop('password')
        
        try:
            # Tenta criar o usuário.
            user = User.objects.create_user(**user_data)
            user.set_password(password) # Define a senha com o hash de segurança
            user.save()
            print(f"Usuário {user.username} criado com sucesso.")
        except IntegrityError:
            # Se o usuário já existir (por exemplo, migração rodada 2x), apenas ignora.
            print(f"Usuário {user_data.get('username')} já existe, ignorando.")
        except Exception as e:
            print(f"Erro ao criar usuário {user_data.get('username')}: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_usuario_email_confirm_token_and_more'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]