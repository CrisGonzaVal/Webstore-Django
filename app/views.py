
from django.shortcuts import render , redirect
from.models import Producto, Inventario, Categoria, Marca
from django.db.models import Sum

from .Carrito import Carrito
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json
import base64

def cantidad_carrito(request):
    carrito = Carrito(request)
    total_carrito = sum(Decimal(str(item['acumulado'])) for item in carrito.carrito.values())

    # Calcular la cantidad total de productos en el carrito
    cantidad_total_productos = sum(item['cantidad'] for item in carrito.carrito.values())
    
    # Contexto común para todas las vistas
    contexto_comun = {
        'carrito': carrito.carrito,
        'total_carrito': total_carrito,
        'cantidad_total_productos': cantidad_total_productos,  # Agrega la cantidad total
    }
    
    return contexto_comun



# se crean las vistas

def home(request):
   # Obtener el contexto común
    contexto_carrito = cantidad_carrito(request)
    
    # Renderizar la plantilla 'carro.html' con el contexto extendido
    return render(request, 'app/home.html', contexto_carrito)


def login(request):

    # Obtener el contexto común
    contexto_carrito = cantidad_carrito(request)
    
    # Renderizar la plantilla 'carro.html' con el contexto extendido
    return render(request, 'app/login.html', contexto_carrito)
   
def registro(request):
    # Obtener el contexto común
    contexto_carrito = cantidad_carrito(request)
    
    # Renderizar la plantilla 'carro.html' con el contexto extendido
    return render(request, 'app/registro.html', contexto_carrito)   

def carro(request):
    # Obtener el contexto común
    contexto_carrito = cantidad_carrito(request)

    carrito_items = [
        {
            'id': key,
            'nombre': item['nombre'],
            'cantidad': item['cantidad'],
            'acumulado': str(item['acumulado']),
            'imagen': item['imagen'],
            'id_marca': item['id_marca'],
            'color': item['color'],
            'valor': str(item.get('valor', '0'))  # Usar get para evitar KeyError
        }
        for key, item in contexto_carrito['carrito'].items()
    ]

    contexto_carrito.update({
        'carrito_items': json.dumps(carrito_items)
    })
    
    # Renderizar la plantilla 'carro.html' con el contexto extendido
    return render(request, 'app/carro.html', contexto_carrito)
 

#manipulo los modelos producto e inventario y lo muestro en la vista catalogo.html
def catalogo(request):
    # Obtener todos los productos
    productos=Producto.objects.all()

    # Obtener filtros de parámetros GET
    marca = request.GET.get('marca')
    categoria = request.GET.get('categoria')
    precio = request.GET.get('precio')
    query = request.GET.get('q', '')  # Obtener la consulta de búsqueda
    

     # Aplicar búsqueda no exacta
    if query:
        productos = productos.filter(nombre_prod__icontains=query)

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

     # Obtener contexto común del carrito
    contexto_carrito = cantidad_carrito(request)

    #actualiza el contecto_carrito y Pasar los productos con la cantidad total calculada al contexto
    contexto_carrito.update({
       'productos': productos,
       'categorias': categorias,
       'marcas': marcas,
       'query': query,
     })
    return render(request, 'app/catalogo.html',contexto_carrito)  



def contactanos(request):
    return render(request, 'app/contactanos.html')  


def ofertas(request):
    # Obtener el contexto común
    contexto_carrito = cantidad_carrito(request)
    
    # Renderizar la plantilla 'carro.html' con el contexto extendido
    return render(request, 'app/ofertas.html', contexto_carrito)


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

def generate_access_token():
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    auth = f"{client_id}:{client_secret}"
    auth_encoded = base64.b64encode(auth.encode()).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
        headers=headers,
        data={'grant_type': 'client_credentials'}
    )

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError(f"Failed to retrieve access token: {response.text}")



@csrf_exempt
def create_order(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            cart = body.get('cart', [])
            total_value = sum(Decimal(item['acumulado']) for item in cart)

            url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {generate_access_token()}',
            }
            payload = {
                'intent': 'CAPTURE',
                'purchase_units': [
                    {
                        'amount': {
                            'currency_code': 'USD',
                            'value': str(total_value),
                        },
                    },
                ],
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()
            return JsonResponse(data, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def capture_order(request, order_id):
    try:
        if request.method == 'POST':
            url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {generate_access_token()}',
            }
            response = requests.post(url, headers=headers)
            data = response.json()
            return JsonResponse(data, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def limpiar_carrito_despues_compra(request):
    if request.method == 'POST':
        carrito = Carrito(request)
        carrito.limpiar()
        return JsonResponse({'status': 'Carrito limpiado después de la compra'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def gracias(request):
    return render(request, 'app/gracias.html')