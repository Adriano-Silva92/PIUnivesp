from django.urls import path
from .views import IndexView, apagar_mensagem
from .views import criar_pedido, exportar_pedidos_csv
from .views import usuarios_logados_partial, negar_pedido, aprovar_pedido
from .views import checar_status_pedidos, exportar_pedidos_pdf


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('apagar-mensagem/<int:mensagem_id>/', apagar_mensagem, name='apagar_mensagem'),
    path('criar-pedido/', criar_pedido, name='criar_pedido'),
    path('usuarios-logados/', usuarios_logados_partial, name='usuarios_logados_partial'),
    path('negar-pedido/<int:pedido_id>/', negar_pedido, name='negar_pedido'),
    path('aprovar-pedido/<int:pedido_id>/', aprovar_pedido, name='aprovar_pedido'),
    path('checar-status-pedidos/', checar_status_pedidos, name='checar_status_pedidos'),
    path('exportar/pdf/', exportar_pedidos_pdf, name='exportar_pdf'),
    path('exportar/csv/', exportar_pedidos_csv, name='exportar_csv'),
    ]