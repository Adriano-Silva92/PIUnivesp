from django.contrib import admin  # Importa o módulo de administração do Django
from django.utils.html import format_html  # Permite renderizar HTML de forma segura no admin
from .models import Pedido, Mensagem, Profile  # Importa os modelos definidos na aplicação


@admin.register(Pedido)
# Define os campos que serão exibidos na listagem de pedidos no painel admin
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'produto', 'status', 'data', 'foto')


@admin.register(Mensagem)
# Define os campos visíveis na listagem de mensagens no admin
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'texto', 'data_criacao')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de perfis
    list_display = ('user', 'last_seen', 'foto')

    # Define campos que não podem ser editados (apenas visualização)
    readonly_fields = ('foto_preview',)

    # Define a ordem e os campos que serão exibidos na página de edição do perfil
    fields = ('user', 'foto', 'foto_preview', 'last_seen')

    # Metodo para exibir uma prévia da imagem da foto de perfil
    def foto_preview(self, obj):
        if obj.foto:
            # Renderiza a imagem em HTML com largura de 100px e bordas arredondadas
            return format_html('<img src="{}" width="100" style="border-radius: 8px;" />', obj.foto.url)
        return "Sem foto"  # Caso o usuário não tenha foto

    # Define o nome do campo no painel admin
    foto_preview.short_description = "Prévia da Foto"

