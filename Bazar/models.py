
from tabnanny import verbose

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_inicial = models.DateField()
    data_final = models.DateField()
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.nome
        
class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='imagens', null=True, blank=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='dono')
    usuario_reserva = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='usuario_reserva')
    evento = models.ManyToManyField(Evento, related_name='evento')
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        
    def __str__(self):
        return self.nome


