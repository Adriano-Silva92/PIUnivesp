from django.utils import timezone

# Middleware personalizado para atualizar o campo `last_seen` (último acesso) do perfil do usuário
class LastSeenMiddleware:
    def __init__(self, get_response):
        # Metodo de inicialização: armazena a função que processa a requisição
        self.get_response = get_response

    def __call__(self, request):
        # Chama a função de resposta (view) para processar a requisição
        response = self.get_response(request)

        # Se o usuário estiver autenticado (logado no sistema)
        if request.user.is_authenticated:
            # Obtém o perfil associado ao usuário (se existir)
            profile = getattr(request.user, 'profile', None)

            # Se o perfil existir, atualiza o campo `last_seen` com a data/hora atual
            if profile:
                profile.last_seen = timezone.now()

                # Salva apenas o campo 'last_seen' no banco para otimizar a operação
                profile.save(update_fields=['last_seen'])

        # Retorna a resposta final
        return response
