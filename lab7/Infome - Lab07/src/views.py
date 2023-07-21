from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PedidoForm, RegistroForm
from .models import Carrito, Pedido, Cliente, Marca, Articulo
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    pedido = Pedido.objects.filter(PedCabCodCli=request.user)
    return render(request, 'index.html', {'pedidos' : pedido})

#Detalle pedido
@login_required
def DetallePedido(request, pedidoID):
    pedido_cabecera = get_object_or_404(Pedido, pk=pedidoID, PedCabCodCli=request.user)
    detalles_pedido = Pedido.objects.filter(PedDetCodCab=pedido_cabecera)

    if detalles_pedido.exists():
        detalle = detalles_pedido.first()
    else:
        detalle = Pedido(PedDetCodCab=pedido_cabecera)

    if request.method == 'GET':
        form = PedidoForm(instance=detalle)
        carrito = request.session.get('carrito', {})
        articulos = Articulo.objects.filter(pk__in=carrito.keys())
        detalles = []
        for articulo in articulos:
            cantidad = carrito[str(articulo.pk)]['cantidad']
            subtotal = cantidad * articulo.ArtPreUni
            detalles.append({
                'articulo': articulo,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        return render(request, 'pedido_detalle.html', {
            'pedido_cabecera': pedido_cabecera,
            'detalle': detalle,
            'form': form,
            'detalles': detalles
        })
    else:
        form = PedidoForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
        

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
    pedido_cabecera = get_object_or_404(Pedido, pk=pedidoID, PedCabCodCli=request.user)
    detalles_pedido = Pedido.objects.filter(pk=pedidoID)

    for detalle in detalles_pedido:
        articulo = detalle.PedDetArtCod
        articulo.ArtSto += detalle.PedDetCantidad 
        articulo.save()

    pedido_cabecera.delete()

    return redirect('index')

#Carrito de compras
@login_required
def agregar_al_carrito(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, articulo=articulo)
    if not created:
        carrito.cantidad += 1
        carrito.save()
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, carrito_id):
    carrito = get_object_or_404(Carrito, pk=carrito_id, usuario=request.user)
    carrito.delete()
    return redirect('carrito')

@login_required
def carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in carrito)
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def actualizar_cantidad(request, item_pk, cantidad):
    carrito_item = get_object_or_404(Carrito, pk=item_pk)
    carrito_item.cantidad = cantidad
    carrito_item.save()
    return JsonResponse({'status': 'ok'})

def cancelar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    request.session['carrito'] = []
    request.session.modified = True
    carrito.delete()
    return redirect('carrito')

@login_required
def guardar_pedido(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    if carrito.exists():
        pedido_cabecera = Pedido(PedCabCodCli=request.user)
        # pedido_cabecera.save()
        for item in carrito:
            articulo = item.articulo
            cantidad = item.cantidad
            if cantidad > articulo.ArtSto:
                messages.error(request, f'La cantidad de "{articulo.ArtNom}" en el carrito supera el stock disponible.')
                return redirect('carrito')
            subtotal = cantidad * articulo.ArtPreUni
            pedido_cabecera.PedDetArtCod = articulo
            pedido_cabecera.PedDetCantidad = cantidad
            pedido_cabecera.PedDetPreUniArt = articulo.ArtPreUni
            pedido_cabecera.PedDetSubtotal = subtotal
            pedido_cabecera.PedDetTot += subtotal
            articulo.ArtSto -= cantidad 
            articulo.save()
            pedido_cabecera.save()
            item.pedido = pedido_cabecera
            item.save()
        carrito.delete()
        # request.session['carrito'] = {}
        return redirect('pedido_detalle', pedidoID=pedido_cabecera.pk)
    
    else:
        messages.warning(request, 'No hay artículos en el carrito.')
        return redirect('index')

#Pedido detalle
def pedido_detalle(request, pedidoID):
    pedido = get_object_or_404(Pedido, pk=pedidoID)
    detalles = Pedido.objects.filter(pk=pedidoID, PedCabCodCli=request.user, PedCabFec=pedido.PedCabFec)
    return render(request, 'pedido_detalle.html', {'pedido': pedido, 'detalles': detalles})

#Productos
def productos(request):
    productos = Articulo.objects.all()
    return render(request, 'productos.html', {'productos': productos})

#Token 
@api_view(['POST'])
def generar_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token = user.generate_auth_token()
        return Response({'token': token})
    else:
        return Response({'error': 'Credenciales inválidas'})


