from django.shortcuts import render, get_object_or_404, redirect
from .models import (Zapatilla, Categoria, Marca, StockZapatilla, 
Usuario, Pedido, Carrito, ItemCarrito, Direccion)
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UsuarioForm, DireccionForm, ZapatillaForm, StockZapatillaForm, UpdateUsuarioForm
from django.core.paginator import Paginator
from django.http import Http404


def index(request):
    productos_nuevos = Zapatilla.objects.all().order_by('-id')[:9]  #ultimos 9 productos
    nike_marca = Marca.objects.get(nombre="Nike")
    productos_nike = Zapatilla.objects.filter(marca=nike_marca).order_by('id')[:9]  #ultimos 9 productos NIKE
    
    data = {
        'productos_nuevos': productos_nuevos,
        'productos_nike': productos_nike
    }
    return render(request, 'aplicacion/index.html', data)

def producto(request, id):
    zapatilla = get_object_or_404(Zapatilla, id=id)
    tallas_disponibles = StockZapatilla.objects.filter(zapatilla=zapatilla)
    productos_relacionados = Zapatilla.objects.filter(categoria__in=zapatilla.categoria.all()).exclude(id=id).distinct()

    datos = {
        'zapatilla': zapatilla,
        'tallas_disponibles': tallas_disponibles,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'aplicacion/producto.html', datos)


def administrador(request):
    zapatillas = Zapatilla.objects.order_by('modelo')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(zapatillas,5) #Muestra 5 productos por pagina
        zapatillas = paginator.page(page)
    except:
        raise Http404
    
    datos = {'entity': zapatillas, #ENTITY ES NECESARIO PARA EL PAGINADOR
            'paginator': paginator}
    
    return render(request,'aplicacion/admin.html',datos)

def detalleproducto(request, id):
    zapatilla = get_object_or_404(Zapatilla, id=id)
    tallas_disponibles = StockZapatilla.objects.filter(zapatilla=zapatilla)
    datos = {
        'zapatilla': zapatilla,
        'tallas_disponibles': tallas_disponibles,
    }

    return render(request, 'aplicacion/detalleproducto.html', datos)


def adminpedido(request):
    return render(request,'aplicacion/adminpedido.html')

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
        paginator = Paginator(zapatillas,10)
        zapatillas = paginator.page(page)
    except:
        raise Http404

    datos = {'entity': zapatillas, 
             'filtro': marca.nombre,
             'paginator': paginator,
             'marca': marca
             }
    return render(request, 'aplicacion/marca.html', datos)

def categoria(request,id):
    categoria = get_object_or_404(Categoria, id=id)
    zapatillas = Zapatilla.objects.filter(categoria=categoria).order_by('modelo')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(zapatillas,10)
        zapatillas = paginator.page(page)
    except:
        raise Http404
    
    datos = {'entity': zapatillas, 
             'filtro': categoria.nombre,
             'paginator': paginator,
             'categoria' : categoria
             }
    
    return render(request,'aplicacion/categoria.html', datos)

def direcciones(request):
    return render(request,'aplicacion/direcciones.html')

def editar(request,id): #editarproducto
    return render(request,'aplicacion/editar.html')



# def login(request):
#     return render(request,'aplicacion/registration/login.html')

def loginAdmin(request):
     return render(request,'aplicacion/loginAdmin.html')

def pedidos(request):
    return render(request,'aplicacion/pedidos.html')

def perfil(request):
    return render(request,'aplicacion/perfil.html')

def recuperar(request):
    return render(request,'aplicacion/recuperar.html')

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

def totalpedidos(request):
    pedidos = Pedido.objects.order_by('-fecha')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(pedidos,5)
        pedidos = paginator.page(page)
    except:
        raise Http404
    
    datos = {'entity' : pedidos, #ENTITY ES NECESARIO PARA EL PAGINADOR
            'paginator': paginator}
    
    return render(request,'aplicacion/totalpedidos.html', datos)

def totalusuarios(request):
    usuarios = Usuario.objects.order_by('-rut')
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(usuarios,5)
        usuarios = paginator.page(page)
    except:
        raise Http404
    
    datos = {'entity': usuarios, #ENTITY ES NECESARIO PARA EL PAGINADOR
             'paginator': paginator}

    return render(request,'aplicacion/totalusuarios.html', datos)

def usuarios(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    datos = {
        'usuario': usuario,
    }
    return render(request,'aplicacion/usuarios.html', datos)

def agregarUsuario(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        direccion_form = DireccionForm(request.POST)
        if usuario_form.is_valid() and direccion_form.is_valid():
            usuario = usuario_form.save()
            direccion = direccion_form.save()
            usuario.direcciones.add(direccion)
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

        return redirect('totalusuarios')

    # Si no es un POST request, renderizar la página de confirmación de eliminación
    return render(request, 'aplicacion/eliminarusuario.html', {'usuario': usuario})

def editarusuarios(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)

    if request.method == 'POST':
        form = UpdateUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect(to="totalusuarios")

    else:
        form = UpdateUsuarioForm(instance=usuario)

    data = {
        'form': form,
        'usuario' : usuario
    }
    return render(request, 'aplicacion/editarusuarios.html', data)

def direccionesusuario(request,rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    direcciones = usuario.direcciones.all()
    data = {
        'usuario': usuario,
        'direcciones': direcciones,
    }
    return render(request, 'aplicacion/direccionesusuario.html',data)

def editardirecciones(request,id):
    direccion = get_object_or_404(Direccion, id=id)
    usuario = direccion.usuario_set.first()  # Obtener el primer usuario asociado a la dirección

    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            return redirect('direccionesusuario', rut=usuario.rut)
    else:
        form = DireccionForm(instance=direccion)

    data = {
        'direccion':direccion,
        'usuario': usuario,
        'form': form,
    }
    return render(request, 'aplicacion/editardirecciones.html', data)

def eliminardireccion(request, id):
    direccion = get_object_or_404(Direccion, id=id)
    rut = direccion.usuario_set.first().rut
    direccion.delete()
    return redirect('editardirecciones', id=id)

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
            stock = StockZapatilla.objects.get(zapatilla=zapatilla, talla=float(talla))
        except StockZapatilla.DoesNotExist:
            return redirect('carrito')  # Manejo de error, redirigir o mostrar mensaje

        carrito = request.session.get('carrito', {})

        # Agregar la zapatilla al carrito
        if str(id_zapatilla) in carrito:
            carrito[str(id_zapatilla)]['cantidad'] += 1
        else:
            carrito[str(id_zapatilla)] = {
                'id': zapatilla.id,
                'modelo': zapatilla.modelo,
                'precio': zapatilla.precio,
                'cantidad': 1,
                'talla': talla,
            }

        # Actualizar la sesión del carrito
        request.session['carrito'] = carrito
        request.session.modified = True
        return redirect('carrito')
    return redirect('detalle_zapatilla', id_zapatilla=id_zapatilla)


def eliminarCarrito(request, id_item):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if str(id_item) in carrito:
            del carrito[str(id_item)]
            request.session['carrito'] = carrito
            request.session.modified = True

    return redirect('carrito')

def confirmarCompra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')

    for item_id, item_info in carrito.items():
        zapatilla = get_object_or_404(Zapatilla, id=item_info['id'])
        stock = get_object_or_404(StockZapatilla, zapatilla=zapatilla, talla=float(item_info['talla']))

        if stock.cantidad >= item_info['cantidad']:
            stock.cantidad -= item_info['cantidad']
            stock.save()
        else:
            # Manejo de error si no hay suficiente stock
            return redirect('carrito')

    # Vaciar el carrito después de confirmar la compra
    request.session['carrito'] = {}
    request.session.modified = True

    return render(request, 'aplicacion/compraconfirmada.html')