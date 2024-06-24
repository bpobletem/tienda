from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Direccion(models.Model):
    calle = models.CharField(max_length=255, null=False)
    numero = models.IntegerField(null=False)
    detalle = models.CharField(max_length=255, null= True, verbose_name="Detalle o Departamento")
    comuna = models.CharField(max_length=255, null=False)
    region = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.detalle}, {self.comuna}, {self.region}"


class Usuario(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    contrasenia = models.CharField(max_length=50, null=False)
    correo = models.EmailField(unique=True, max_length=254, null=False)
    fnac = models.DateField(verbose_name="Fecha de Nacimiento", null=False)
    direcciones = models.ManyToManyField(Direccion)
    telefono = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.rut} -- {self.nombre} {self.apellido}"


class Marca(models.Model):
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"{self.nombre}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"{self.nombre}"
    
class Zapatilla(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50, null=False)
    precio = models.IntegerField(null=False)
    categoria = models.ManyToManyField(Categoria)
    descripcion = models.CharField(max_length=500, null=False)
    foto = models.ImageField(upload_to='zapatillas')

    def __str__(self):
        return f"{self.marca} -- {self.modelo}"

class StockZapatilla(models.Model):
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE)
    talla = models.DecimalField(decimal_places=1, max_digits=3, null=False)
    cantidad = models.IntegerField(null=False, default=0)

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"Carrito de {self.usuario}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE )
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True, null=True) #Hay que sacar el null

    def __str__(self):
        return f"{self.cantidad} - {self.zapatilla.modelo}"

    def precioTotal(self):
        return self.cantidad * self.zapatilla.precio

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Completado'),
        ('A', 'Anulado'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    zapatillas = models.ManyToManyField(Zapatilla, through='PedidoZapatilla')
    estado = models.CharField(max_length=1, choices=ESTADOS_PEDIDO, default='P')
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"


class PedidoZapatilla(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Pedido {self.pedido.id} - {self.zapatilla.modelo} (Cantidad: {self.cantidad})"


class Administrador(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    contrasenia = models.CharField(max_length=50, null=False)
    correo = models.EmailField(unique=True, max_length=254)

    def __str__(self):
        return f"{self.rut} -- {self.nombre} {self.apellido}"
