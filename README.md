## 🛠️ Projeto Integrador Univesp - Sistema de Gerenciamento de Pedidos

Projeto desenvolvido com Django para gerenciamento de pedidos, com interface moderna e responsiva utilizando HTML, CSS e Bootstrap. 

## 📌 Descrição

O projeto trata se de um sistema web para registrar, visualizar e controlar pedidos, voltado para uso interno em organizações. Permite aos usuários autenticados solicitarem produtos, acompanhar o status dos pedidos, visualizar mensagens em tempo real e ainda conta com uma API para envios de e-mails automáticos. Também possui suporte ao Cloudnary com 25GB de armazenamento de imagens na nuvem. 

Link acesso: https://technikpi.fly.dev/ (Acesso por tempo limitado)

## 🚀 Funcionalidades

- 📦 Cadastro de pedidos com prioridade e status
- 👤 Gerenciamento de usuários (login e logout)
- 🧾 Visualização de pedidos e mensagens em tempo real
- 💬 Sistema de mensagens estilo chat
- 🌙 Suporte a tema escuro/claro com persistência
- 📈 Gráficos interativos com Chart.js
- 🖼️ Upload e visualização de fotos de perfil com Cloudinary
- 🔐 Painel administrativo Django para superusuários
- 🖨️ Exportação de dados (PDF/CSV)

## 📷 Imagens do sistema

![Pedidos](https://github.com/user-attachments/assets/414c143b-a92d-4dc4-866a-6eaf924c5e74); 
![NovoPedido](https://github.com/user-attachments/assets/c310b57e-3e66-4746-a75c-e3eb187f99f0);
![PedidoAprovado ](https://github.com/user-attachments/assets/2419a58d-7c2a-470f-8304-18e5e1aa1ac2);
![VisaoSuperUser](https://github.com/user-attachments/assets/27bf42e6-edd1-4501-be75-2a102cf8ae93);


## 🧰 Tecnologias utilizadas

- Python 3.11
- Django 4.x
- HTML5 + CSS3
- Bootstrap 4
- JavaScript (DOM, localStorage)
- Chart.js
- SweetAlert2
- Cloudinary (armazenamento de imagens)
- PostgreSQL
- Docker / Docker Compose
- Fly.io (Deploy)

## ⚙️ Instalação e execução local

```bash
# Clone o repositório
git clone https://github.com/Adriano-Silva92/PIUnivesp.git
cd PIUnivesp

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo .env com as configurações do ambiente

# Rode as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
