from decimal import Decimal

def total_carrito(request):
    total = Decimal('0.00')
    if request.user.is_authenticated:
        carrito = request.session.get("carrito", {})
        for key, value in carrito.items():
            total += Decimal(str(value["acumulado"]))
    return {"total_carrito": total}


