# Generated by Django 5.2.2 on 2025-06-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_remove_lotebipagem_group_user_fk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotebipagem',
            name='group_user_txt',
            field=models.CharField(default='grupo_padrao', max_length=100),
        ),
    ]
