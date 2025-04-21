from django.contrib import admin
from django.utils.html import format_html
from .models import Pedido, Mensagem, Profile


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'produto', 'status', 'data')


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'texto', 'data_criacao')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_seen', 'foto')
    readonly_fields = ('foto_preview',)
    fields = ('user', 'foto', 'foto_preview', 'last_seen')

    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="100" style="border-radius: 8px;" />', obj.foto.url)
        return "Sem foto"

    foto_preview.short_description = "Prévia da Foto"
