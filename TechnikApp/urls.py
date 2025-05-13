# Importa o metodo path para definir rotas, e include para incluir rotas de outros apps.
from django.urls import path, include

# Importa as views que serão usadas nas rotas.
from .views import IndexView, apagar_mensagem, excluir_pedido
from .views import criar_pedido, exportar_pedidos_csv
from .views import usuarios_logados_partial, negar_pedido, aprovar_pedido
from .views import checar_status_pedidos, exportar_pedidos_pdf
from .views import verificar_novas_mensagens

# Lista de URLs da aplicação
urlpatterns = [
    # Rota principal da aplicação. Usa uma view baseada em classe para exibir a página inicial.
    path('', IndexView.as_view(), name='index'),

    # Rota para apagar uma mensagem pelo seu ID.
    path('apagar-mensagem/<int:mensagem_id>/', apagar_mensagem, name='apagar_mensagem'),

    # Rota para criação de um novo pedido.
    path('criar-pedido/', criar_pedido, name='criar_pedido'),

    # Rota que retorna uma partial com os usuários logados (pode ser usada por HTMX ou Ajax).
    path('usuarios-logados/', usuarios_logados_partial, name='usuarios_logados_partial'),

    # Rota para negar um pedido específico pelo seu ID.
    path('negar-pedido/<int:pedido_id>/', negar_pedido, name='negar_pedido'),

    # Rota para aprovar um pedido específico pelo seu ID.
    path('aprovar-pedido/<int:pedido_id>/', aprovar_pedido, name='aprovar_pedido'),

    # Rota para excluir um pedido específico pelo seu ID.
    path('excluir_pedido/<int:pedido_id>/', excluir_pedido, name='excluir_pedido'),

    # Rota usada para checar o status dos pedidos (provavelmente para atualização dinâmica).
    path('checar-status-pedidos/', checar_status_pedidos, name='checar_status_pedidos'),

    # Rota para exportar os pedidos em formato PDF.
    path('exportar/pdf/', exportar_pedidos_pdf, name='exportar_pdf'),

    # Rota para exportar os pedidos em formato CSV.
    path('exportar/csv/', exportar_pedidos_csv, name='exportar_csv'),

    path('verificar-novas-mensagens/', verificar_novas_mensagens, name='verificar_novas_mensagens'),

    # Inclui as rotas necessárias para transformar o projeto em um Progressive Web App (PWA).
    path('', include('pwa.urls')),
]
