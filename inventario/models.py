from django.db import models

class LoteBipagem(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
        ('processando', 'Processando'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')

    def __str__(self):
        return f"Lote #{self.id}"