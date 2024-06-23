from django.shortcuts import render, get_object_or_404, redirect
from .models import Zapatilla, Categoria, Marca, StockZapatilla, Usuario, Pedido
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UsuarioForm, DireccionForm, ZapatillaForm, StockZapatillaForm
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.
def index(request):
    return render(request,'aplicacion/index.html')

def producto(request, id):
    zapatilla = get_object_or_404(Zapatilla, id=id)
    tallas_disponibles = StockZapatilla.objects.filter(zapatilla=zapatilla)
    datos = {
        'zapatilla': zapatilla,
        'tallas_disponibles': tallas_disponibles
    }
    return render(request,'aplicacion/producto.html', datos)

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

def editar(request): #editarproducto
    return render(request,'aplicacion/editar.html')

def editarusuarios(request, rut):
    usuario = get_object_or_404(Usuario, rut=rut)
    
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('aplicacion/usuarios.html')  # Asumiendo que tienes una vista para listar usuarios
    else:
        form = UsuarioForm(instance=usuario)

    datos = {
        'form': form, 'usuario': usuario
    }
    
    return render(request, 'aplicacion/editarusuarios.html', datos)

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

    return render(request, 'registration/registro.html', {
        'usuario_form': usuario_form,
        'direccion_form': direccion_form,
    })

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

def carrito(request):
    return render(request,'aplicacion/carrito.html')

