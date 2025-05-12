## 🛠️ PI Univesp - Sistema de Gerenciamento de Pedidos

Projeto desenvolvido com Django para gerenciamento de pedidos, com interface moderna e responsiva utilizando HTML, CSS e Bootstrap.

## 📌 Descrição

O **PIUnivesp** é um sistema web para registrar, visualizar e controlar pedidos, voltado para uso interno em organizações. Permite aos usuários autenticados solicitarem produtos, acompanhar o status dos pedidos e visualizar mensagens em tempo real.

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


## 🧰 Tecnologias utilizadas

- Python 3.11
- Django 4.x
- HTML5 + CSS3
- Bootstrap 4
- JavaScript (DOM, localStorage)
  * Chart.js
  * SweetAlert2
- Cloudinary (Armazenamento de Imagens)
- PostgreSQL (Banco de Dados)
- Docker / Docker Compose 
- Fly.io (Deploy)

<p align="left"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="30" title="Python 3.11"/> Python 3.11 &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="30" title="Django 4.x"/> Django 4.x &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="30" title="HTML5"/> HTML5 &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="30" title="CSS3"/> CSS3 &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-plain.svg" width="30" title="Bootstrap 4"/> Bootstrap 4 &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="30" title="JavaScript"/> JavaScript &nbsp; <img src="https://www.chartjs.org/media/logo-title.svg" width="40" title="Chart.js"/> Chart.js &nbsp; <img src="https://sweetalert2.github.io/images/SweetAlert2.png" width="30" title="SweetAlert2"/> SweetAlert2 &nbsp; <img src="https://appexchange.salesforce.com/image_host/300c831a-4271-44f2-91da-b48269175229.png" width="40" title="Cloudinary"/> Cloudinary &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="30" title="PostgreSQL"/> PostgreSQL &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="30" title="Docker"/> Docker &nbsp; <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThhJ-RtJkPOQdeJCnyGe2dbicjNlPgYStxYw&s" width="30" title="Fly.io"/> Fly.io </p>

## ⚙️ Instalação e execução local

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
