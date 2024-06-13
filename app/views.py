from django.shortcuts import render, redirect
from .models import Producto
from .Carrito import Carrito  
from decimal import Decimal

# se crean las vistas
def home(request):
    return render(request, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')

def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    return render(request, 'app/carro.html') 

def catalogo(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/catalogo.html', data)  

def contactanos(request):
    return render(request, 'app/contactanos.html')  

def ofertas(request):
    return render(request, 'app/ofertas.html')  

def proveedores(request):
    return render(request, 'app/proveedores.html')   

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)  
    carrito.agregar(producto)
    return redirect("carro")

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




def carro(request):
    carrito = Carrito(request)
    context = {
        'carrito': carrito.carrito,
        'total_carrito': sum(Decimal(str(item['acumulado'])) for item in carrito.carrito.values())
    }
    return render(request, 'app/carro.html', context)

