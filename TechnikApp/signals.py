from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def criar_profile_automatico(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_profile_automatico(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
