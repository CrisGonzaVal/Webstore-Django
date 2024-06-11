
from django.shortcuts import render 
from.models import Producto, Inventario
from django.db.models import Sum


# se crean las vistas
def home(request):
   return render(request, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')
   
def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    return render(request, 'app/carro.html') 

#manipulo los modelos producto e inventario y lo muestro en la vista catalogo
def catalogo(request):
    # Obtener todos los productos
    productos=Producto.objects.all()

    # Calcular la cantidad total de cada producto
    # consulta usando python que es = select cantidad AS sum(cantidad_total) FROM Inventario WHERE id_producto = producto.id_producto
    for producto in productos:
        cantidad_total = Inventario.objects.filter(id_producto=producto).aggregate(total=Sum('cantidad'))['total']
        producto.cantidad_total = cantidad_total if cantidad_total is not None else 0

    # Pasar los productos con la cantidad total calculada al contexto
    data={
       'productos': productos
    }
    return render(request, 'app/catalogo.html',data)  

def contactanos(request):
    return render(request, 'app/contactanos.html')  

def ofertas(request):
    return render(request, 'app/ofertas.html')  

def proveedores(request):
    return render(request, 'app/proveedores.html')   


