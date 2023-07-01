from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

# Vendedor 
class Vendedor(models.Model):
    VenDNI = models.CharField(max_length=8, unique=True)
    VenApePat = models.CharField(max_length=20)
    VenNom = models.CharField(max_length=20)
    VenEstReg = models.BooleanField(default=True)
    #Mostrar nombre del vendedor
    def __str__(self):
        nombre = self.VenNom + ' ' +self.VenApePat
        return nombre
    
#Cliente
class Cliente(AbstractUser):
    CliDNI = models.CharField(max_length=8)
    CliApePat = models.CharField(max_length=20)
    CliNom = models.CharField(max_length=20)
    CliEstReg = models.BooleanField(default=True)

    # Mostrar nombre completo del cliente
    def __str__(self):
        return self.CliNom + ' ' + self.CliApePat
    
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=150, unique=True, null=True)

#Marca
class Marca(models.Model):
    MarNom = models.CharField(max_length=20)
    MarImg = models.ImageField(upload_to='imagenes/imgs', null=True)
    MarEstReg = models.BooleanField(default=True)
    #Mostrar nombre de las marcas
    def __str__(self):
        return self.MarNom

#Tipo Artículo
class TipoArticulo(models.Model):
    TipArtNom = models.CharField(max_length=20)
    TipArtEstReg = models.BooleanField(default=True)
    #Mostrar nombre de los tipos de artículos
    def __str__(self):
        return self.TipArtNom

#Articulo 
class Articulo(models.Model):
    ArtMarCod = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True)
    ArtTipCod = models.ForeignKey(TipoArticulo, on_delete=models.CASCADE, null=True)
    ArtNom = models.CharField(max_length=50, null=True)
    ArtDes = models.TextField(max_length=1000, help_text='Ingresa la descripción del artículo', null=True)
    ArtImg = models.ImageField(upload_to='imagenes/imgs', null=True)
    ArtSto = models.IntegerField()
    ArtPreUni = models.FloatField()
    ArtEstReg = models.BooleanField(default=True)
    #Mostrar nombre del Artículo
    def __str__(self):
        return self.ArtNom 

#Pedido Cabecera
class PedidoCabecera(models.Model):
    PedCabCodCli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    PedCabCodVen = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    PedCabFec = models.DateField(auto_now=False, auto_now_add=False)
    PedCabEstReg = models.BooleanField(default=True)
    #Mostrar pedido cabecera
    def __str__(self):
        return str(self.PedCabCodCli)

#Pedido Detalle
class PedidoDetalle(models.Model):
    PedDetCodCab = models.ForeignKey(PedidoCabecera, on_delete=models.CASCADE, related_name='detalles')
    PedDetArtCod = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    PedDetCantidad = models.IntegerField(default=1)
    PedDetPreUniArt = models.FloatField(default=0.0)
    PedDetSubtotal = models.FloatField(default=0.0)
    PedDetTot = models.FloatField(default=0.0)
    PedDetEstReg = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Obtener el precio del artículo seleccionado
        precio_articulo = self.PedDetArtCod.ArtPreUni

        # Actualizar el campo PedDetPreUniArt con el precio del artículo
        self.PedDetPreUniArt = precio_articulo

        # Calcular el subtotal y el total
        self.PedDetSubtotal = self.PedDetCantidad * self.PedDetPreUniArt
        self.PedDetTot = self.PedDetSubtotal

        super().save(*args, **kwargs)
        
    #Mostrar pedido detalle 
    def __str__(self):
        return str(self.PedDetCodCab)