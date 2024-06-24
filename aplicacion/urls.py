from django.urls import path, include
from .views import (index, producto,administrador, detalleproducto, loginAdmin, 
                    adminpedido,anadir,categoria,direcciones,editar,editarusuarios,pedidos,
                    perfil,recuperar,registro,totalpedidos,totalusuarios,usuarios,carrito,marca, 
                    agregarCarrito, eliminarCarrito, confirmarCompra, agregarUsuario
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('producto/<int:id>/', producto, name='producto'),
    path('administrador/', administrador, name='admin'),
    path('detalleproducto/<int:id>', detalleproducto, name='detalleproducto'),
    path('adminpedido/', adminpedido, name='adminpedido'),
    path('anadir/', anadir, name='anadir'),
    path('categoria/<int:id>/', categoria, name='categoria'),
    path('marca/<int:id>/', marca, name='marca'),
    path('direcciones/', direcciones, name='direcciones'),
    path('editar/<int:id>', editar, name='editar'),
    path('editarusuarios/<str:rut>', editarusuarios, name='editarusuarios'),
    # path('login/', login, name='login'),
    path('loginAdmin/', loginAdmin, name='loginAdmin'),
    path('pedidos/', pedidos, name='pedidos'),
    path('perfil/', perfil, name='perfil'),
    path('recuperar/', recuperar, name='recuperar'),
    path('registro/', registro, name='registro'),
    path('totalpedidos/', totalpedidos, name='totalpedidos'),
    path('totalusuarios/', totalusuarios, name='totalusuarios'),
    path('usuarios/<str:rut>', usuarios, name='usuarios'),
    path('carrito/', carrito, name='carrito'),
    path('carrito/<int:id_zapatilla>/', agregarCarrito, name='agregarCarrito'),
    path('carrito/<int:id_item>', eliminarCarrito, name='eliminarCarrito'),
    path('compraconfirmada/', confirmarCompra, name="confirmarCompra"),
    path('agregarusuario/', agregarUsuario, name="agregarUsuario")
] 

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
