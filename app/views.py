from django.shortcuts import render, redirect
from .models import Producto
from .Carrito import Carrito
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json

# se crean las vistas
def home(request):
    return render(request, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')

def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    carrito = Carrito(request)
    carrito_items = [
        {
            'id': key,
            'nombre': item['nombre'],
            'cantidad': item['cantidad'],
            'acumulado': str(item['acumulado']),
            'imagen': item['imagen'],
            'id_marca': item['id_marca'],
            'color': item['color'],
            'valor': str(item['valor'])
        }
        for key, item in carrito.carrito.items()
    ]
    context = {
        'carrito': carrito.carrito,
        'carrito_items': json.dumps(carrito_items),  # Convert to JSON string
        'total_carrito': sum(Decimal(str(item['acumulado'])) for item in carrito.carrito.values())
    }
    return render(request, 'app/carro.html', context)

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


@csrf_exempt
def create_order(request):
    try:
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
                        'value': '100',  # This value should be dynamic
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

def generate_access_token():
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    auth = (client_id, client_secret)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials'}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=payload, auth=auth)
    data = response.json()
    return data['access_token']
