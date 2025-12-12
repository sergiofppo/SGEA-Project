# GoEvents! - Sistema de Gestão de Eventos Acadêmicos

O GoEvents! é um sistema web completo desenvolvido em Django para o gerenciamento de eventos acadêmicos, como seminários, palestras e minicursos. O projeto foi expandido para incluir autenticação robusta, APIs REST e auditoria de ações.

## ✨ Funcionalidades Principais (Fase 2 Implementada)

* **Identidade Visual:** Aplicação da identidade visual GoEvents! nas páginas e certificados.
* **Autenticação Avançada:** Sistema de cadastro que exige **Confirmação de E-mail** antes da ativação da conta.
* **Perfis e Acessos:** Perfis distintos (Aluno, Professor, Organizador) com regras de negócio claras para inscrição e acesso.
* **Gerenciamento de Eventos:** CRUD (Criação, Leitura, Edição, Exclusão) completo de eventos por **Organizadores**.
    * **Validações:** Regras de negócio implementadas, como proibição de cadastrar eventos com data passada e obrigatoriedade do campo Apresentador.
    * **Recursos Visuais:** Suporte para upload de **Banner** nos eventos.
* **Auditoria (Logs):** Registro de todas as ações críticas (Criação de Usuário, CRUD de Eventos, Inscrições, Geração/Consulta de Certificados).
* **API RESTful:** Desenvolvida utilizando Django Rest Framework para:
    * Consulta de Eventos (limitada a 20 requisições/dia).
    * Inscrição de Participantes (limitada a 50 requisições/dia).
    * Autenticação via Token (necessária para todas as requisições da API).
* **Inscrição e Certificados:** Inscrição em eventos com controle de vagas e regras de perfil. Emissão e download automático de certificados em PDF.
* **Busca Inteligente:** Funcionalidade de busca que filtra eventos por nome, apresentador ou tipo.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python com o framework Django.
* **API:** Django Rest Framework (DRF).
* **Frontend:** HTML5, TailwindCSS para estilização e JavaScript para funcionalidades dinâmicas (máscara de formulário).
* **Banco de Dados:** SQLite 3 (padrão do Django para desenvolvimento).
* **Geração de PDF:** Biblioteca `reportlab` com `Pillow`.

## ⚙️ Guia de Instalação e Testes (Guia de Testes/Instalação)

Siga os passos abaixo para rodar o projeto em seu ambiente de desenvolvimento.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/miguellferraz/SGEA-Project
    cd SGEA_Project
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv venv
    venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário (administrador):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Execute o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

O sistema estará disponível em `http://127.0.0.1:8000`.

### Roteiro de Testes Funcionais (Seeding)

Para testar as funcionalidades com perfis predefinidos:

| Usuário | Login | Senha | Perfil | URL de Teste |
| :--- | :--- | :--- | :--- | :--- |
| Organizador | `organizador@sgea.com` | `Admin@123` | ORGANIZADOR | Gerenciar Eventos, Acessar Logs |
| Professor | `professor@sgea.com` | `Professor@123` | PROFESSOR | Inscrição em Eventos |
| Aluno | `aluno@sgea.com` | `Aluno@123` | ALUNO | Inscrição e Download de Certificados |

**Nota sobre E-mail:** Após o cadastro de novos usuários, verifique a janela do terminal onde o servidor está rodando para visualizar o link de ativação da conta (Console Backend).
