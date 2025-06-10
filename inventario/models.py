from django.db import models

class LoteBipagem(models.Model):
    id=models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
        ('processando', 'Processando'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    user_created = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True)
    group_user = models.CharField(max_length=100, default='grupo_padrao')

class Caixa(models.Model):
    id=models.AutoField(primary_key=True)
    nr_caixa = models.CharField(max_length=100,null=True)
    lote = models.ForeignKey(LoteBipagem, on_delete=models.CASCADE, related_name='caixas')
    identificador = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Caixa {self.identificador} (Lote #{self.lote.id})"