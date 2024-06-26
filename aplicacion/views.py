from django.shortcuts import render, get_object_or_404, redirect
from .models import (Zapatilla, Categoria, Marca, StockZapatilla,
                     Usuario, Pedido, PedidoZapatilla, Carrito, ItemCarrito, Direccion, )
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import (UsuarioForm, DireccionForm, ZapatillaForm,
                    StockZapatillaForm, UpdateUsuarioForm, AdminLoginForm, SearchForm, PedidoForm, PedidoZapatillaFormSet)
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from django.contrib import messages

def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='loginAdmin',  # URL de la vista de login de administradores
        redirect_field_name=None
    )
    return actual_decorator(view_func)

def search_results(request):
    query = request.GET.get('query')
    results = []
    page = request.GET.get('page', 1)


    if query:
        results = Zapatilla.objects.filter(
                Q(modelo__icontains=query) |  Q(marca__nombre__icontains=query)
            )

        try:
            paginator = Paginator(results,5)
            results = paginator.page(page)
        except:
            raise Http404
    
    data = {
        'paginator': paginator,
        'entity' : results,
        'query' : query
    }
    return render(request, 'aplicacion/searchproduct.html', data)

def index(request):
    productos_nuevos = Zapatilla.objects.all().order_by(
        '-id')[:9]  # ultimos 9 productos
    nike_marca = Marca.objects.get(nombre="Nike")
    productos_nike = Zapatilla.objects.filter(marca=nike_marca).order_by('id')[
        :9]  # ultimos 9 productos NIKE

    data = {
        'productos_nuevos': productos_nuevos,
        'productos_nike': productos_nike
    }
    return render(request, 'aplicacion/index.html', data)


def producto(request, id):
    zapatilla = get_object_or_404(Zapatilla, id=id)
    tallas_disponibles = StockZapatilla.objects.filter(zapatilla=zapatilla)
    productos_relacionados = Zapatilla.objects.filter(
        categoria__in=zapatilla.categoria.all()).exclude(id=id).distinct()

    datos = {
        'zapatilla': zapatilla,
        'tallas_disponibles': tallas_disponibles,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'aplicacion/producto.html', datos)

@admin_required
def administrador(request):
    zapatillas = Zapatilla.objects.order_by('modelo')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(zapatillas, 5)  # Muestra 5 productos por pagina
        zapatillas = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': zapatillas,  # ENTITY ES NECESARIO PARA EL PAGINADOR
             'paginator': paginator}

    return render(request, 'aplicacion/admin.html', datos)


@admin_required
def detalleproducto(request, id):
    zapatilla = get_object_or_404(Zapatilla, id=id)
    tallas_disponibles = StockZapatilla.objects.filter(zapatilla=zapatilla)
    datos = {
        'zapatilla': zapatilla,
        'tallas_disponibles': tallas_disponibles,
    }

    return render(request, 'aplicacion/detalleproducto.html', datos)

@admin_required
def adminpedido(request):
    return render(request, 'aplicacion/adminpedido.html')


def listaPedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'aplicacion/listaPedidos.html', {'pedidos': pedidos})


def crearPedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = PedidoZapatillaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            formset.instance = pedido
            formset.save()
            messages.success(request, 'Pedido creado con exito')
            return redirect('listaPedidos')
    else:
        form = PedidoForm()
        formset = PedidoZapatillaFormSet()
    return render(request, 'aplicacion/crearPedido.html', {'form': form, 'formset': formset})


def editarPedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = PedidoZapatillaFormSet(request.POST, instance=pedido)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Pedido editado con exito')
            return redirect('listaPedidos')
    else:
        form = PedidoForm(instance=pedido)
        formset = PedidoZapatillaFormSet(instance=pedido)
    return render(request, 'aplicacion/editarPedido.html', {'form': form, 'formset': formset})


def eliminarPedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado con exito')
        return redirect('listaPedidos')
    return render(request, 'aplicacion/eliminarPedido.html', {'pedido': pedido})


def detallePedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'aplicacion/detallePedido.html', {'pedido': pedido})


@admin_required
def anadir(request):
    if request.method == 'POST':
        zapatilla_form = ZapatillaForm(request.POST, request.FILES)
        stock_form = StockZapatillaForm(request.POST)
        if zapatilla_form.is_valid() and stock_form.is_valid():
            zapatilla = zapatilla_form.save()
            stock = stock_form.save(commit=False)
            stock.zapatilla = zapatilla
            stock.save()
            return redirect('administrador')
    else:
        zapatilla_form = ZapatillaForm()
        stock_form = StockZapatillaForm()

    datos = {
        'zapatilla_form': zapatilla_form,
        'stock_form': stock_form
    }
    return render(request, 'aplicacion/anadir.html', datos)


def marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    zapatillas = Zapatilla.objects.filter(marca=marca).order_by('modelo')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(zapatillas, 10)
        zapatillas = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': zapatillas,
             'filtro': marca.nombre,
             'paginator': paginator,
             'marca': marca
             }
    return render(request, 'aplicacion/marca.html', datos)


def categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    zapatillas = Zapatilla.objects.filter(
        categoria=categoria).order_by('modelo')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(zapatillas, 10)
        zapatillas = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': zapatillas,
             'filtro': categoria.nombre,
             'paginator': paginator,
             'categoria': categoria
             }

    return render(request, 'aplicacion/categoria.html', datos)


@login_required
def direcciones(request,rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    direcciones = usuario.direcciones.all()
    data = {
        'usuario': usuario,
        'direcciones': direcciones,
    }
    return render(request,'aplicacion/direcciones.html', data)

@login_required
def agregardireccionusuario(request,rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save()
            usuario.direcciones.add(direccion)
            messages.success(request, 'Direccion agregada con exito')
            return redirect('direcciones', rut=usuario.rut)
    else:
        form = DireccionForm()

    data = {
        'form': form,
        'usuario': usuario
    }

    return render(request, 'aplicacion/agregardireccionusuario.html', data)

@login_required
def editardireccionusuario(request, id):
    direccion = get_object_or_404(Direccion, id=id)
    usuario = direccion.usuario_set.first()

    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Direccion editada con exito')
            return redirect('direccionesusuario', rut=usuario.rut)
    else:
        form = DireccionForm(instance=direccion)

    data = {
        'direccion':direccion,
        'usuario': usuario,
        'form': form,
    }
    return render(request, 'aplicacion/editardireccionusuario.html', data)

@login_required
def eliminardireccionusuario(request,id):
    direccion = get_object_or_404(Direccion, id=id)
    usuario = direccion.usuario_set.first()
    if usuario:
        usuario.direcciones.remove(direccion)
    direccion.delete()
    messages.success(request, 'Direccion eliminada con exito')
    return redirect('direcciones', rut=usuario.rut)


def editar(request,id): #editarproducto
    return render(request,'aplicacion/editar.html')


def editar(request, id):  # editarproducto
    return render(request, 'aplicacion/editar.html')


# def login(request):
#     return render(request,'aplicacion/registration/login.html')

def loginAdmin(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin')  # Redirigir a la página de administrador después del login
    else:
        form = AdminLoginForm()

    data = {
        'form' : form
    }

    return render(request, 'aplicacion/loginAdmin.html', data)

def pedidos(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    pedidos = Pedido.objects.filter(cliente=usuario)
    data = {
        'usuario':usuario,
        'pedidos':pedidos
    }
    return render(request,'aplicacion/pedidos.html', data)

@login_required
def perfil(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    if request.method == 'POST':
        form = UpdateUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil editado con exito')
            return redirect(to="perfil", rut=usuario.rut)

    else:
        form = UpdateUsuarioForm(instance=usuario)

    data = {
        'form': form,
        'usuario' : usuario
    }
    return render(request,'aplicacion/perfil.html', data)

def recuperar(request):
    return render(request, 'aplicacion/recuperar.html')


def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        direccion_form = DireccionForm(request.POST)
        if usuario_form.is_valid() and direccion_form.is_valid():
            usuario = usuario_form.save()
            direccion = direccion_form.save()
            usuario.direcciones.add(direccion)
            return redirect('index')
    else:
        usuario_form = UsuarioForm()
        direccion_form = DireccionForm()

    data = {
        'usuario_form': usuario_form,
        'direccion_form': direccion_form,
    }

    return render(request, 'registration/registro.html', data)

@admin_required
def totalpedidos(request):
    pedidos = Pedido.objects.order_by('-fecha')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(pedidos, 5)
        pedidos = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': pedidos,  # ENTITY ES NECESARIO PARA EL PAGINADOR
             'paginator': paginator}

    return render(request, 'aplicacion/totalpedidos.html', datos)


@admin_required
def totalusuarios(request):
    usuarios = Usuario.objects.order_by('-rut')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(usuarios, 5)
        usuarios = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': usuarios,  # ENTITY ES NECESARIO PARA EL PAGINADOR
             'paginator': paginator}

    return render(request, 'aplicacion/totalusuarios.html', datos)


@admin_required
def usuarios(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    datos = {
        'usuario': usuario,
    }
    return render(request, 'aplicacion/usuarios.html', datos)


@admin_required
def agregarUsuario(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        direccion_form = DireccionForm(request.POST)
        if usuario_form.is_valid() and direccion_form.is_valid():
            usuario = usuario_form.save()
            direccion = direccion_form.save()
            usuario.direcciones.add(direccion)
            messages.success(request, 'Usuario agregado con exito')
            return redirect('totalusuarios')
    else:
        usuario_form = UsuarioForm()
        direccion_form = DireccionForm()

    data = {
        'usuario_form': usuario_form,
        'direccion_form': direccion_form,
    }

    return render(request, 'aplicacion/agregarusuario.html', data)

def eliminarUsuario(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)

    if request.method == 'POST':
        # Eliminar todos los pedidos asociados al usuario
        pedidos = Pedido.objects.filter(cliente=usuario)
        for pedido in pedidos:
            pedido.delete()

        # Eliminar todas las direcciones asociadas al usuario
        usuario.direcciones.clear()

        # Eliminar el usuario
        usuario.delete()
        messages.success(request, 'Usuario eliminado con exito')
        return redirect('totalusuarios')

    # Si no es un POST request, renderizar la página de confirmación de eliminación
    return render(request, 'aplicacion/eliminarusuario.html', {'usuario': usuario})

def editarusuarios(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)

    if request.method == 'POST':
        form = UpdateUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado con exito')
            return redirect(to="totalusuarios")

    else:
        form = UpdateUsuarioForm(instance=usuario)

    data = {
        'form': form,
        'usuario': usuario
    }
    return render(request, 'aplicacion/editarusuarios.html', data)

def direccionesusuario(request,rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    direcciones = usuario.direcciones.all()
    data = {
        'usuario': usuario,
        'direcciones': direcciones,
    }
    return render(request, 'aplicacion/direccionesusuario.html', data)


def agregardireccion(request,rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save()
            usuario.direcciones.add(direccion)
            messages.success(request, 'Direccion agregada con exito')
            return redirect('direccionesusuario', rut=usuario.rut)
    else:
        form = DireccionForm()

    data = {
        'form': form,
        'usuario': usuario
    }

    return render(request, 'aplicacion/agregardireccion.html', data)


def editardirecciones(request,id):
    direccion = get_object_or_404(Direccion, id=id)
    usuario = direccion.usuario_set.first()

    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Direccion editada con exito')
            return redirect('direccionesusuario', rut=usuario.rut)
    else:
        form = DireccionForm(instance=direccion)

    data = {
        'direccion': direccion,
        'usuario': usuario,
        'form': form,
    }
    return render(request, 'aplicacion/editardirecciones.html', data)

def eliminardireccion(request, id):
    direccion = get_object_or_404(Direccion, id=id)
    usuario = direccion.usuario_set.first()
    if usuario:
        usuario.direcciones.remove(direccion)
    direccion.delete()
    messages.success(request, 'Direccion eliminada con exito')
    return redirect('direccionesusuario', rut=usuario.rut)

def carrito(request):
    carrito = request.session.get('carrito', {})
    zapatillas_en_carrito = []
    total_carrito = 0

    for item_id, item_info in carrito.items():
        zapatilla = get_object_or_404(Zapatilla, id=item_info['id'])
        subtotal = item_info['cantidad'] * zapatilla.precio
        total_carrito += subtotal

        zapatillas_en_carrito.append({
            'zapatilla': zapatilla,
            'cantidad': item_info['cantidad'],
            'subtotal': subtotal,
            'talla': item_info['talla'],
        })

    datos = {
        'zapatillas_en_carrito': zapatillas_en_carrito,
        'total_carrito': total_carrito,
    }
    return render(request, 'aplicacion/carrito.html', datos)

def agregarCarrito(request, id_zapatilla):
    if request.method == 'POST':
        talla = request.POST.get('talla_seleccionada')
        zapatilla = get_object_or_404(Zapatilla, id=id_zapatilla)

        # Verificar si la talla es válida
        if not talla:
            return redirect('detalle_zapatilla', id_zapatilla=zapatilla.id)

        talla = talla.replace(',', '.')

        # Obtener el stock para la zapatilla y la talla específica
        try:
            stock = StockZapatilla.objects.get(
                zapatilla=zapatilla, talla=float(talla))
        except StockZapatilla.DoesNotExist:
            # Manejo de error, redirigir o mostrar mensaje
            return redirect('carrito')

        carrito = request.session.get('carrito', {})

        # Construir el identificador único para la zapatilla y la talla
        carrito_item_id = f"{id_zapatilla}_{talla}"

        # Verificar si el artículo ya está en el carrito
        if carrito_item_id in carrito:
            carrito[carrito_item_id]['cantidad'] += 1
        else:
            carrito[carrito_item_id] = {
                'id': zapatilla.id,
                'modelo': zapatilla.modelo,
                'precio': zapatilla.precio,
                'cantidad': 1,
                'talla': talla,
            }

        # Actualizar la sesión del carrito
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, 'Item agregado al carrito con exito')
        return redirect('carrito')

    return redirect('detalle_zapatilla', id_zapatilla=id_zapatilla)

@login_required
def eliminarCarrito(request, carrito_item_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        # Verifica si el carrito_item_id está en el carrito
        if carrito_item_id in carrito:
            del carrito[carrito_item_id]
            request.session['carrito'] = carrito
            request.session.modified = True

    return redirect('carrito')

def confirmarCompra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')

    for item_id, item_info in carrito.items():
        zapatilla = get_object_or_404(Zapatilla, id=item_info['id'])
        stock = get_object_or_404(
            StockZapatilla, zapatilla=zapatilla, talla=float(item_info['talla']))

        if stock.cantidad >= item_info['cantidad']:
            stock.cantidad -= item_info['cantidad']
            stock.save()
        else:
            # Manejo de error si no hay suficiente stock
            return redirect('carrito')

    # Vaciar el carrito después de confirmar la compra
    request.session['carrito'] = {}
    request.session.modified = True
    messages.success(request, 'Gracias por tu compra')
    return render(request, 'aplicacion/compraconfirmada.html')
