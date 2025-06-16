from django.db import models

class LoteBipagem(models.Model):
    id=models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
        ('aguardando validação', 'Aguardando Validação'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberto')
    user_created = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True)
    group_user = models.CharField(max_length=100, default='grupo_padrao')

class Caixa(models.Model):
    id=models.AutoField(primary_key=True)
    nr_caixa = models.CharField(max_length=100,null=True)
    lote = models.ForeignKey(LoteBipagem, on_delete=models.CASCADE, related_name='caixas')
    identificador = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('iniciada', 'Iniciada'),
        ('finalizada', 'Finalizada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Iniciada')

    def __str__(self):
        return f"Caixa {self.identificador} (Lote #{self.lote.id})"
    
class Bipagem(models.Model):
    id=models.AutoField(primary_key=True)
    id_caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name='bipagem')
    id_lote = models.ForeignKey(LoteBipagem, on_delete=models.CASCADE, related_name='bipagem')
    unidade = models.IntegerField(null=True)
    nrserie = models.CharField(max_length=50,null=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    modelo = models.CharField(max_length=100, null=True)
    patrimonio = models.CharField(max_length=100, null=True)

class Serial(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    lote = models.ForeignKey(LoteBipagem, on_delete=models.CASCADE, related_name='seriais')

    def __str__(self):
        return self.codigo