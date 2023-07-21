"""
URL configuration for localstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tienda import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
 # from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('home/', views.Home, name='home'),
    path('signup/', views.Signup, name='signup'),
    path('index/', views.Index, name='index'),
    # path('index/crear_pedido/', views.CreatePedido, name='crear_pedido'),
    path('index/<int:pedidoID>/', views.DetallePedido, name='pedido_detalle'),
    # path('index/actualizar/<int:pedidoID>/', views.Actualizar_pedido, name='actualizar_pedido'),
    path('index/eliminar/<int:pedidoID>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('logout/', views.Signout, name='logout'),
    path('signin/', views.Signin, name='signin'),
    path('agregar_al_carrito/<int:articulo_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('actualizar_cantidad/<int:item_pk>/<int:cantidad>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar_del_carrito/<int:carrito_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('guardar_pedido/', views.guardar_pedido, name='guardar_pedido'),
    path('pedido_detalle/<int:pedidoID>/', views.pedido_detalle, name='pedido_detalle'),
    path('productos/', views.productos, name='productos'),
    path('marca/<int:marca_id>/', views.marca_detail, name='marca_detail'),
    path('cancelar_carrito/', views.cancelar_carrito, name='cancelar_carrito'),
    path('', include('tienda.urls')),
    path('api-token-auth/', views.generar_token),
    # path('api-token-auth/', views.obtain_auth_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
