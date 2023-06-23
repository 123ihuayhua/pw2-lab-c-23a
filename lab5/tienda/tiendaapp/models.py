from django.db import models
# Vendedor
class Vendedor(models.Model):
    VenDNI = models.CharField(max_length=8, unique=True)
    VenApePat = models.CharField(max_length=20)
    VenNom = models.CharField(max_length=20)
    VenEstReg = models.BooleanField(default=True)

    # Mostrar nombre del vendedor
    def __str__(self):
        nombre = self.VenNom + ' ' + self.VenApePat
        return nombre


# Cliente
class Cliente(models.Model):
    CliDNI = models.CharField(max_length=8, unique=True)
    CliApePat = models.CharField(max_length=20)
    CliNom = models.CharField(max_length=20)
    CliEstReg = models.BooleanField(default=True)

    # Mostrar DNI del cliente
    def __str__(self):
        return self.CliNom + ' ' + self.CliApePat


# Marca
class Marca(models.Model):
    MarNom = models.CharField(max_length=20)
    MarEstReg = models.BooleanField(default=True)
    # Mostrar nombre de las marcas
    def __str__(self):
        return self.MarNom


# Tipo Artículo
class TipoArticulo(models.Model):
    TipArtNom = models.CharField(max_length=20)
    TipArtEstReg = models.BooleanField(default=True)
    # Mostrar nombre de los tipos de artículos
    def __str__(self):
        return self.TipArtNom

# Articulo
class Articulo(models.Model):
    ArtMarCod = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True)
    ArtTipCod = models.ForeignKey(TipoArticulo, on_delete=models.CASCADE, null=True)
    ArtNom = models.CharField(max_length=50, null=True)
    ArtDes = models.TextField(max_length=1000, help_text='Ingresa la descripción del artículo', null=True)
    ArtSto = models.IntegerField(default=0)
    ArtPreUni = models.FloatField(default=0)
    ArtEstReg = models.BooleanField(default=True)
    Img = models.TextField(default='')
    # Mostrar nombre del Artículo
    def __str__(self):
        return self.ArtNom

# Pedido Cabecera
class PedidoCabecera(models.Model):
    PedCabCodCli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    PedCabCodVen = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    PedCabFec = models.DateField(auto_now=False, auto_now_add=False)
    PedCabEstReg = models.BooleanField(default=True)

    # Mostrar pedido cabecera
    def __str__(self):
        return str(self.PedCabCodCli)


# Pedido Detalle
class PedidoDetalle(models.Model):
    PedDetCodCab = models.ForeignKey(PedidoCabecera, on_delete=models.CASCADE, related_name='detalles')
    PedDetArtCod = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    PedDetCantidad = models.IntegerField(default=0)
    PedDetPreUniArt = models.FloatField(default=0.0)
    PedDetSubtotal = models.FloatField(default=0.0)
    PedDetTot = models.FloatField(default=0.0)
    PedDetEstReg = models.BooleanField(default=True)

    # Mostrar pedido detalle
    def __str__(self):
        return str(self.PedDetCodCab)

    # Calculo automático
    def save(self, *args, **kwargs):
        self.PedDetPreUniArt = self.PedDetArtCod.ArtPreUni
        self.PedDetSubtotal = self.PedDetCantidad * self.PedDetPreUniArt
        super().save(*args, **kwargs)

    @staticmethod
    def actualizar_total_pedido(pedido_cabecera):
        detalles = pedido_cabecera.detalles.all()
        total_pedido = sum(detalle.PedDetSubtotal for detalle in detalles)
        pedido_cabecera.PedCabTot = total_pedido
        pedido_cabecera.save()