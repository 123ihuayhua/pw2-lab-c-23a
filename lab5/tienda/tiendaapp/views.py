from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import *
from .forms import *
#Vista principal
def Home(request):
    return render(request, 'home.html')


def Signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': RegistroForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario
                user = Cliente.objects.create_user(username=request.POST['username'],
                                                   password=request.POST['password1'])
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
def otro(request):
    marcas = Marca.objects.all()
    articulos = Articulo.objects.all()
    objetosPorMarca = []
    for marca in marcas:
        articulosEnMarca = []
        for art in articulos:
            if art.ArtMarCod == marca:
                articulosEnMarca.append(art.Img)
        objetosPorMarca.append(articulosEnMarca)
    context = {
        'arr':objetosPorMarca
    }
    return render(request,'articulos/test.html',context)
def second(*args,**kwargs):
    return HttpResponse('<h1>Este es 2do</h1>')