# Generated by Django 5.2 on 2025-04-07 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnikApp', '0005_alter_pedido_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='visto_pelo_usuario',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='produto',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='setor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
