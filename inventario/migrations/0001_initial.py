# Generated by Django 5.2.2 on 2025-06-09 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoteBipagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('aberto', 'Aberto'), ('fechado', 'Fechado'), ('processando', 'Processando')], default='aberto', max_length=20)),
            ],
        ),
    ]
