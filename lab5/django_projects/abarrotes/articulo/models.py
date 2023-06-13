from django.db import models

# Create your models here.
class Articulo(models.Model):
    codigo = models.PositiveIntegerField()
    codigoMarca = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    precioUnitario = models.PositiveIntegerField()
    estadoRegistro = models.TextField()

