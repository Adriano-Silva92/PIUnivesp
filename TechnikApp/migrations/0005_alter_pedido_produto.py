# Generated by Django 5.2 on 2025-04-05 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnikApp', '0004_alter_pedido_produto_alter_pedido_setor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='produto',
            field=models.CharField(max_length=50),
        ),
    ]
