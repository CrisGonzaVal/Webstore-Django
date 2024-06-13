from decimal import Decimal
from .Carrito import Carrito


def total_carrito(request):
    total = Decimal('0.00')
    if request.user.is_authenticated:
        carrito = request.session.get("carrito", {})
        for key, value in carrito.items():
            total += Decimal(str(value["acumulado"]))
    return {"total_carrito": total}


def carrito_total(request):
    carrito = Carrito(request)
    total_items = sum(item['cantidad'] for item in carrito.carrito.values())
    return {'total_carrito': total_items}
