from django.contrib import admin
from .models import *


class AdmUsuario(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido','contrasenia', 'correo', 'fnac']
    list_editable = ['nombre', 'apellido', 'fnac', 'contrasenia', 'correo']

class AdmZapatilla(admin.ModelAdmin):
    list_display = ['id', 'marca', 'modelo', 'precio', 'descripcion']
    list_editable = ['marca', 'modelo', 'precio', 'descripcion']


class AdmDireccion(admin.ModelAdmin):
    list_display = ['id', 'calle', 'numero', 'comuna']
    list_editable = ['calle', 'numero', 'comuna']


class AdmMarca(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    list_editable = ['nombre']

class AdmPedido(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'estado']

class AdmCategoria(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    list_editable = ['nombre']

class AdmPedidoZapatilla(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'zapatilla', 'cantidad']

class AdmAdministrador(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido','contrasenia', 'correo']
    list_editable = ['nombre', 'apellido','contrasenia', 'correo']

class AdmStockZapatillas(admin.ModelAdmin):
    list_display= ['id', 'zapatilla','talla','cantidad']
    list_editable= ['zapatilla','talla','cantidad']
    list_display_links = ['id']
    
# Register your models here.
admin.site.register(Usuario, AdmUsuario)
admin.site.register(Zapatilla, AdmZapatilla)
admin.site.register(Direccion, AdmDireccion)
admin.site.register(Marca, AdmMarca)
admin.site.register(Pedido, AdmPedido)
admin.site.register(Categoria, AdmCategoria)
admin.site.register(PedidoZapatilla, AdmPedidoZapatilla)
admin.site.register(Administrador, AdmAdministrador)
admin.site.register(StockZapatilla, AdmStockZapatillas)
