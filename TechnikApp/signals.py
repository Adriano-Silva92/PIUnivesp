# Importa o sinal post_save, que é disparado após a chamada do metodo save() em um modelo.
from django.db.models.signals import post_save
# Importa o decorador receiver, usado para conectar funções a sinais.
from django.dispatch import receiver
# Importa o modelo User padrão do Django, que representa os usuários do sistema.
from django.contrib.auth.models import User
# Importa o modelo Profile, que está relacionado ao User (normalmente com OneToOneField).
from .models import Profile


# Conecta a função abaixo ao sinal post_save do modelo User.
# Essa função será executada sempre que um novo usuário for criado.
@receiver(post_save, sender=User)
def criar_profile_automatico(sender, instance, created, **kwargs):
    # Verifica se o usuário foi criado (e não apenas atualizado).
    if created:
        # Cria automaticamente um Profile relacionado ao novo usuário.
        Profile.objects.create(user=instance)


# Conecta outra função ao mesmo sinal post_save do modelo User.
# Essa função será executada após qualquer salvamento de um usuário.
@receiver(post_save, sender=User)
def salvar_profile_automatico(sender, instance, **kwargs):
    # Verifica se o usuário tem um profile associado antes de tentar salvar.
    if hasattr(instance, 'profile'):
        # Salva o profile do usuário, útil se ele foi modificado indiretamente.
        instance.profile.save()
