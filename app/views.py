
from django.shortcuts import render 
from.models import Producto, Inventario, Categoria, Marca
from django.db.models import Sum, Q


# se crean las vistas
def home(request):
   return render(request, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')
   
def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    return render(request, 'app/carro.html') 


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

    # Pasar los productos con la cantidad total calculada al contexto
    data={
       'productos': productos,
       'categorias': categorias,
       'marcas': marcas
    }
    return render(request, 'app/catalogo.html',data)  



def ofertas(request):
    return render(request, 'app/ofertas.html')  




