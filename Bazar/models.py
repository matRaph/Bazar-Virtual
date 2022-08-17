from tokenize import blank_re

from django.contrib.auth.models import User
from django.db import models
from pyexpat import model

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='imagens', null=True, blank=True)
    dono = models.ForeignKey(Usuario, on_delete=models.CASCADE, 
        related_name='dono')
    usuario_reserva = models.ForeignKey(Usuario, on_delete=models.CASCADE, 
        null=True, blank=True, related_name='usuario_reserva')

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_inicial = models.DateField()
    data_final = models.DateField()

    def __str__(self):
        return self.nome
