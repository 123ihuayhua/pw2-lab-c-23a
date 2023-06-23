from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import *
# Create your views here.
def myHomeView(request,*args,**kwargs):
    '''print(args,kwargs)
    print(request.user)'''
    myContext = {
        'myText':'Esto es un texto sobre nosotros',
        'myNumber':7,
        'myList':[33,44,55],
    }
    #return render(request,'home.html',{})#{} ES EL CONTEXTO
    return render(request,'home.html',myContext)
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