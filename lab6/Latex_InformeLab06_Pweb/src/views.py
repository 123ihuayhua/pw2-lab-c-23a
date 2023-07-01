from datetime import date
import datetime
from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PedidoDetForm, PedidoForm, RegistroForm
from django.forms import formset_factory, ValidationError
from .models import PedidoCabecera, PedidoDetalle, Cliente, Marca, Articulo, Vendedor
from django.contrib.auth.decorators import login_required 

# Create your views here.
#Vista principal
def Home(request):
    marcas = Marca.objects.all()
    arts = Articulo.objects.all()
    context = {'marcas': marcas, 'arts': arts}
    return render(request, 'home.html', context)

#Registrarse (usuario)
def Signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': RegistroForm})

    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario
                user = Cliente.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # Guardar usuario 
                user.CliDNI = request.POST['CliDNI']
                user.CliApePat = request.POST['CliApePat']
                user.CliNom = request.POST['CliNom']
                user.CliEstReg = True
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': RegistroForm,
                    'error': 'El usuario ya existe'
                })
            
        return render(request, 'signup.html', {
            'form': RegistroForm,
            'error': 'Las contraseñas no coinciden'
        })
    
@login_required
#Ver pedidos
def Index(request):
    pedido = PedidoCabecera.objects.filter(PedCabCodCli=request.user)
    return render(request, 'index.html', {'pedidos' : pedido})

        # initial=[{'PedCabCodCli': request.user.pk}]

#Crear pedido
PedidoFormSet = formset_factory(PedidoForm, extra=1)
@login_required
def CreatePedido(request):
    if request.method == 'GET':
        vendedores = Vendedor.objects.all()
        articulos = Articulo.objects.all()
        formset = PedidoFormSet(prefix='pedidos')
        form2 = PedidoDetForm(prefix='pedido_det')
        formset.forms[0].initial['PedCabCodCli'] = request.user.pk 
        return render(request, 'pedido.html', {
            'formset': formset,
            'form2': form2,
            'vendedores': vendedores,
            'articulos': articulos
        })
    else:
        formset = PedidoFormSet(request.POST, prefix='pedidos')
        form2 = PedidoDetForm(request.POST, prefix='pedido_det')
        vendedores = Vendedor.objects.all()
        articulos = Articulo.objects.all()
        if formset.is_valid() and form2.is_valid():
            pedido_cab = None
            for form in formset:
                new_pedido = form.save(commit=False)
                new_pedido.PedCabCodCli = get_object_or_404(Cliente, id=request.user.pk)
                if not pedido_cab:
                    pedido_cab = new_pedido
                    pedido_cab.save()
                new_pedido.PedDetCodCab = pedido_cab
                new_pedido.save()
            new_pedido2 = form2.save(commit=False)
            new_pedido2.PedCabCodCli = get_object_or_404(Cliente, id=request.user.pk)
            new_pedido2.PedDetCodCab = pedido_cab
            articulo = new_pedido2.PedDetArtCod
            cantidad = new_pedido2.PedDetCantidad
            if cantidad > articulo.ArtSto:
                return render(request, 'pedido.html', {
                    'formset': formset,
                    'form2': form2,
                    'vendedores': vendedores,
                    'articulos': articulos,
                    'error': f'No hay suficiente stock de {articulo.ArtNom}'
                })
            articulo.ArtSto = articulo.ArtSto - cantidad
            articulo.save()
            new_pedido2.save()
            return redirect('index')
        else:
            return render(request, 'pedido.html', {
                'formset': formset,
                'form2': form2,
                'vendedores': vendedores,
                'articulos': articulos,
                'error': 'Ingrese datos válidos'
            })

#Detalle pedido
@login_required
def DetallePedido(request, pedidoID):
    pedido_cabecera = get_object_or_404(PedidoCabecera, pk=pedidoID, PedCabCodCli=request.user)
    detalles_pedido = PedidoDetalle.objects.filter(PedDetCodCab=pedido_cabecera)

    if detalles_pedido.exists():
        detalle = detalles_pedido.first()
    else:
        detalle = PedidoDetalle(PedDetCodCab=pedido_cabecera)

    if request.method == 'GET':
        form = PedidoDetForm(instance=detalle)
        return render(request, 'pedido_det.html', {'pedido_cabecera': pedido_cabecera, 'detalle': detalle, 'form': form})
    # else:
    #     form = PedidoDetForm(request.POST, instance=detalle)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('index')
    #     return render(request, 'pedido_det.html', {'pedido_cabecera': pedido_cabecera, 'detalle': detalle, 'form': form, 'error': 'No se puede actualizar'})

#Actualizar pedido
@login_required
def Actualizar_pedido(request, pedidoID):
    pedido_cabecera = get_object_or_404(PedidoCabecera, pk=pedidoID, PedCabCodCli=request.user)
    detalles_pedido = PedidoDetalle.objects.filter(PedDetCodCab=pedido_cabecera)

    if detalles_pedido.exists():
        detalle = detalles_pedido.first()
    else:
        detalle = PedidoDetalle(PedDetCodCab=pedido_cabecera)

    if request.method == 'POST':
        form = PedidoDetForm(request.POST, instance=detalle)
        if form.is_valid():
            detalle = form.save(commit=False)
            articulo = detalle.PedDetArtCod
            old_cantidad = detalle.PedDetCantidad
            new_cantidad = form.cleaned_data['PedDetCantidad']
            difference = new_cantidad - old_cantidad
            
            if new_cantidad > articulo.ArtSto:
                error_message = 'La cantidad solicitada supera el stock disponible'
                return render(request, 'actualizar_pedido.html', {'form': form, 'error_message': error_message})
            else:
                articulo.ArtSto = articulo.ArtSto - difference
                articulo.save()
                detalle.save()  # Guardar el objeto PedidoDetalle actualizado en la base de datos
                return redirect('pedido_detalle', pedidoID=pedidoID)
    else:
        form = PedidoDetForm(instance=detalle)

    if pedido_cabecera.PedCabCodCli != request.user:
        return HttpResponseForbidden()
    
    return render(request, 'actualizar_pedido.html', {'form': form})
    # return render(request, 'actualizar_pedido.html', {'form': form})


#Salir de la sesión
def Signout(request):
    logout(request)
    return redirect('home')

#Logearse
def Signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form' : AuthenticationForm
        })
    else:
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
            'form' : AuthenticationForm, 
            'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('index')

#Marcas
def marca_detail(request, marca_id):
    marca = get_object_or_404(Marca, pk=marca_id)
    arts = Articulo.objects.filter(ArtMarCod=marca)
    templates = {
        'Acer': 'marca_acer.html',
        'Apple': 'marca_apple.html',
        'Asus': 'marca_asus.html',
        'Dell': 'marca_dell.html',
        'HP': 'marca_hp.html',
        'Lenovo': 'marca_lenovo.html',
        'MSI': 'marca_msi.html',
    }
    templates = templates.get(marca.MarNom, 'marca_default.html')
    context = {'marca': marca, 'arts': arts}
    return render(request, f'{templates}', context)

#Elimininar pedido
@login_required
def eliminar_pedido(request, pedidoID):
    pedido_cabecera = get_object_or_404(PedidoCabecera, pk=pedidoID, PedCabCodCli=request.user)
    detalles_pedido = PedidoDetalle.objects.filter(PedDetCodCab=pedido_cabecera)

    for detalle in detalles_pedido:
        articulo = detalle.PedDetArtCod
        articulo.ArtSto += detalle.PedDetCantidad
        articulo.save()

    pedido_cabecera.delete()

    return redirect('index')
