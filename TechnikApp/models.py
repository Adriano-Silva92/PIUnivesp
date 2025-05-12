from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import date
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import MediaCloudinaryStorage

# ---------------------------
# Modelo Profile
# ---------------------------

# Representa o perfil de um usuário com foto e última atividade.
class Profile(models.Model):
    # Cria uma relação 1-para-1 com o modelo User do Django.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Campo de imagem para foto de perfil, salva no Cloudinary.
    foto = models.ImageField(
        upload_to='fotos/',  # Caminho dentro do Cloudinary
        storage=MediaCloudinaryStorage(),  # Armazenamento usando Cloudinary
        blank=True,  # Campo opcional
        null=True    # Campo pode ser nulo
    )

    # Data/hora da última vez que o usuário foi visto online.
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    # Propriedade que retorna a URL da foto (ou imagem padrão se não houver)
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return static('img/user_padrao.png')  # Imagem padrão local


# ---------------------------
# Modelo Pedido
# ---------------------------

# Representa um pedido de item feito por um usuário.
class Pedido(models.Model):
    # Definição das prioridades possíveis
    PRIORIDADES = (
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
    )

    # Definição dos status possíveis
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado'),
    )

    # Definição dos tipos possíveis
    TIPO_CHOICES = (
        ('Compra', 'Compra'),
        ('Suporte', 'Suporte'),
    )

    # Usuário que criou o pedido
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Setor do usuário
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    # Nome do produto solicitado
    produto = models.CharField(max_length=100)

    # Quantidade solicitada (inteiro positivo)
    quantidade = models.PositiveIntegerField()

    # Prioridade do pedido
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES)

    # Status atual do pedido
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pendente')

    # Slug único para identificar o pedido (usado em URLs)
    slug = models.SlugField(unique=True, blank=True, max_length=150)

    # Data de criação do pedido (preenchida automaticamente)
    data = models.DateField(auto_now_add=True)

    # Indica se o pedido já foi visualizado pelo usuário
    visto_pelo_usuario = models.BooleanField(default=True)

    # Campo de imagem para foto de perfil, salva no Cloudinary.
    foto = models.ImageField(
        upload_to='fotos-produtos/',  # Caminho dentro do Cloudinary
        storage=MediaCloudinaryStorage(),  # Armazenamento usando Cloudinary
        blank=True,  # Campo opcional
        null=True    # Campo pode ser nulo
    )

    # Método sobrescrito para gerar slug automaticamente com base no usuário, produto e data
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.usuario.username}-{self.produto}-{date.today()}")
            slug = base_slug
            num = 1
            # Garante que o slug seja único (evita conflitos)
            while Pedido.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto} - {self.usuario.username}"

    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return static('img/sem_foto.png')  # fallback para imagem local padrão


# ---------------------------
# Modelo Mensagem
# ---------------------------

# Representa uma mensagem enviada por um usuário (tipo chat).
class Mensagem(models.Model):
    # Usuário que enviou a mensagem
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Texto da mensagem
    texto = models.TextField()

    # Indica se a mensagem já foi lida
    lida = models.BooleanField(default=False)

    # Data de criação da mensagem
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.usuario.username}"

    # Propriedade para exibir a data no formato DD/MM/AAAA
    @property
    def data_lida(self):
        return self.data_criacao.strftime('%d/%m/%Y')

    # Propriedade para retornar a foto do perfil (ou imagem padrão)
    @property
    def foto_url(self):
        profile = getattr(self.usuario, 'profile', None)
        if profile and profile.foto and hasattr(profile.foto, 'url'):
            return profile.foto.url
        return static('img/user_padrao.png')

    # Validação: impede mensagens em branco ou só com espaços
    def clean(self):
        if not self.texto.strip():
            raise ValidationError('O texto da mensagem não pode estar vazio.')

    # Ordenação padrão das mensagens: mais recentes primeiro
    class Meta:
        ordering = ['-data_criacao']
