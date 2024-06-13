from decimal import Decimal
from .Carrito import Carrito

def carrito_context(request):
    carrito = Carrito(request)
    total_items = sum(item['cantidad'] for item in carrito.carrito.values())
    total_acumulado = Decimal('0.00')
    
    if request.user.is_authenticated:
        for item in carrito.carrito.values():
            total_acumulado += Decimal(str(item["acumulado"]))
    
    return {
        'total_items_carrito': total_items,
        'total_acumulado_carrito': total_acumulado,
    }
