
from django.shortcuts import render , redirect
from.models import Producto, Inventario, Categoria, Marca
from django.db.models import Sum, Q

from .Carrito import Carrito
from decimal import Decimal


# se crean las vistas
def home(request):
   return render(request, 'app/home.html',)

def login(request):
    return render(request, 'app/login.html')
   
def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    carrito = Carrito(request)
    context = {
        'carrito': carrito.carrito,
        'total_carrito': sum(Decimal(str(item['acumulado'])) for item in carrito.carrito.values())
    } 
    return render(request,'app/carro.html', context) 


#manipulo los modelos producto e inventario y lo muestro en la vista catalogo.html
def catalogo(request):
    # Obtener todos los productos
    productos=Producto.objects.all()

    # Obtener filtros de parámetros GET
    marca = request.GET.get('marca')
    categoria = request.GET.get('categoria')
    precio = request.GET.get('precio')

    # Aplicar filtros si están presentes
    if marca:
        productos = productos.filter(id_marca__nombre_m=marca)

    if categoria:
        productos = productos.filter(id_categoria__nombre=categoria)

    if precio == 'asc':
        productos = productos.order_by('valor')
    elif precio == 'desc':
        productos = productos.order_by('-valor')

    # Calcular la cantidad total de cada producto
    # consulta usando python que es = select cantidad AS sum(cantidad_total) FROM Inventario WHERE id_producto = producto.id_producto
    for producto in productos:
        cantidad_total = Inventario.objects.filter(id_producto=producto).aggregate(total=Sum('cantidad'))['total']
        producto.cantidad_total = cantidad_total if cantidad_total is not None else 0


        # Obtener listas para los filtros
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

     # almacenas el numero de productos del carrito de compras
    carrito = Carrito(request)

    # Pasar los productos con la cantidad total calculada al contexto
    data={
       'productos': productos,
       'categorias': categorias,
       'marcas': marcas,

       'carrito': carrito.carrito,
       'total_carrito': sum(Decimal(str(item['acumulado'])) for item in carrito.carrito.values())
    }
    return render(request, 'app/catalogo.html',data)  



def ofertas(request):
    return render(request, 'app/ofertas.html')  


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.agregar(producto)
    return redirect("carro")

def agregar_producto_catalogo(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.agregar(producto)
    return redirect("catalogo")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.eliminar(producto)
    return redirect("carro")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.disminuir(producto)
    return redirect("carro")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carro")

