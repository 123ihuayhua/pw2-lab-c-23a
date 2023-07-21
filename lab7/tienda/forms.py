from datetime import timezone
import json
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, formset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, Vendedor
from .models import Cliente


class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cliente
        fields = ('username', 'password1', 'password2',
                  'CliDNI', 'CliApePat', 'CliNom')
        labels = {
            'CliDNI': 'DNI',
            'CliApePat': 'Apellido Paterno',
            'CliNom': 'Nombre'
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        if initial:
            self.fields['PedDetArtCod'].initial = initial['PedDetArtCod'][0]
            self.fields['PedDetCantidad'].initial = initial['PedDetCantidad'][0]
            self.fields['PedDetPreUniArt'].initial = initial['PedDetPreUniArt'][0]
            self.fields['PedDetSubtotal'].initial = initial['PedDetSubtotal'][0]
            self.fields['PedDetTot'].initial = initial['PedDetTot'][0]

    def save(self, commit=True):
        pedido_cabecera = super().save(commit=False)
        pedido_cabecera.PedCabFec = timezone.now()  # Establecer la fecha actual
        if commit:
            pedido_cabecera.save()
        return pedido_cabecera

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         # object is being created
    #         self.actualizar_stock(self.PedDetArtCod, self.PedDetCantidad)
    #     else:
    #         # object is being updated
    #         old_detalle = Pedido.objects.get(pk=self.pk)
    #         if old_detalle.PedDetCantidad != self.PedDetCantidad:
    #             difference = self.PedDetCantidad - old_detalle.PedDetCantidad
    #             self.actualizar_stock(self.PedDetArtCod, difference)
    #     super().save(*args, **kwargs)


@receiver(post_save, sender=Pedido)
def update_stock_quantity(sender, instance, **kwargs):
    articulo = instance.PedDetArtCod
    # articulo.ArtSto = articulo.ArtSto - instance.PedDetCantidad
    articulo.save()


@receiver(post_save, sender=Pedido)
def actualizar_stock(sender, instance, **kwargs):
    articulo = instance.PedDetArtCod
    cantidad = instance.PedDetCantidad
    if cantidad > articulo.ArtSto:
        # error_message = 'La cantidad solicitada supera el stock disponible'
        # return render(request, 'actualizar_pedido.html', {'form': formatter, 'error_message': error_message})
        raise forms.ValidationError(
            f'No hay suficiente stock de {articulo.ArtNom}')
    articulo.ArtSto = articulo.ArtSto - (cantidad-1)
    articulo.save()
