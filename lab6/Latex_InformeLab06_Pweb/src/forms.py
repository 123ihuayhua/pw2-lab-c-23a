from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, formset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import PedidoCabecera 
from .models import PedidoDetalle
from .models import Cliente

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cliente
        fields = ('username', 'password1', 'password2', 'CliDNI', 'CliApePat', 'CliNom')
        labels = {
            'CliDNI': 'DNI', 
            'CliApePat': 'Apellido Paterno',
            'CliNom': 'Nombre'
        }

class PedidoForm(ModelForm):
    class Meta:
        model = PedidoCabecera
        exclude = ['PedCabCodCli']
        fields = ['PedCabCodCli', 'PedCabCodVen', 'PedCabFec']
        labels = {
            'PedCabCodCli': 'Cliente',
            'PedCabCodVen': 'Vendedor',
            'PedCabFec': 'Fecha'
        }
        widgets = {
            'PedCabFec': forms.DateInput(attrs={'type': 'date', 'format': 'YY-MM-DD'})
        }


class PedidoDetForm(ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['PedDetArtCod', 'PedDetCantidad']
        labels = {
            'PedDetArtCod': 'Artículo',
            'PedDetCantidad': 'Cantidad',
        }
        def clean(self):
            cleaned_data = super().clean()
            articulo = cleaned_data.get('PedDetArtCod')
            cantidad = cleaned_data.get('PedDetCantidad')
            if articulo and cantidad:
                if cantidad > articulo.stock:
                    raise forms.ValidationError(f'No hay suficiente stock de {articulo.nombre}')
                # Update the stock in the database
                articulo.stock -= cantidad
                articulo.save()
            return cleaned_data
        
        def save(self, *args, **kwargs):
            if self.pk is None:
                # object is being created
                self.actualizar_stock(self.PedDetArtCod, self.PedDetCantidad)
            else:
                # object is being updated
                old_detalle = PedidoDetalle.objects.get(pk=self.pk)
                if old_detalle.PedDetCantidad != self.PedDetCantidad:
                    difference = self.PedDetCantidad - old_detalle.PedDetCantidad
                    self.actualizar_stock(self.PedDetArtCod, difference)
            super().save(*args, **kwargs)


@receiver(post_save, sender=PedidoDetalle)
def update_stock_quantity(sender, instance, **kwargs):
    articulo = instance.PedDetArtCod
    # articulo.ArtSto = articulo.ArtSto - instance.PedDetCantidad
    articulo.save()

@receiver(post_save, sender=PedidoDetalle)
def actualizar_stock(sender, instance, **kwargs):
    articulo = instance.PedDetArtCod
    cantidad = instance.PedDetCantidad
    if cantidad > articulo.ArtSto:
        # error_message = 'La cantidad solicitada supera el stock disponible'
        # return render(request, 'actualizar_pedido.html', {'form': formatter, 'error_message': error_message})
        raise forms.ValidationError(f'No hay suficiente stock de {articulo.nombre}')
    articulo.ArtSto = articulo.ArtSto - (cantidad-1) 
    articulo.save()

