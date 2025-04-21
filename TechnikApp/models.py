from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import date
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import MediaCloudinaryStorage

# Profile para cadastro de usuario com foto
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(
        upload_to='fotos/',
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True
    )
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return static('img/user_padrao.png')

# Modelo de Pedido
class Pedido(models.Model):
    PRIORIDADES = (
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
    )

    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    setor = models.CharField(max_length=100)
    produto = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pendente')
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    data = models.DateField(auto_now_add=True)
    visto_pelo_usuario = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.usuario.username}-{self.produto}-{date.today()}")
            slug = base_slug
            num = 1
            while Pedido.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto} - {self.usuario.username}"
#Classe Mensagem
class Mensagem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.usuario.username}"

    @property
    def data_lida(self):
        return self.data_criacao.strftime('%d/%m/%Y')  # Criação de data no chat

    @property
    def foto_url(self):
        profile = getattr(self.usuario, 'profile', None)
        if profile and profile.foto and hasattr(profile.foto, 'url'):
            return profile.foto.url
        return static('img/user_padrao.png')

    def clean(self):
        if not self.texto.strip():
            raise ValidationError('O texto da mensagem não pode estar vazio.')

    class Meta:
        ordering = ['-data_criacao']