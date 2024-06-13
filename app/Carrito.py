from decimal import Decimal

class Carrito:
    def __init__(self, request):
        self.session = request.session
        self.carrito = self.session.get("carrito")
        if not self.carrito:
            self.carrito = self.session["carrito"] = {}

    def agregar(self, producto):
        id = str(producto.id_producto)
        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id_producto,
                "nombre": producto.nombre_prod,
                "acumulado": str(producto.valor),
                "cantidad": 1,
                "imagen": producto.imagen.url,
                "color": producto.color,
                "id_marca": str(producto.id_marca)
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] = str(Decimal(self.carrito[id]["acumulado"]) + producto.valor)
        self.guardar_carrito()

    def disminuir(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito:
            if self.carrito[id]["cantidad"] > 1:
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] = str(Decimal(self.carrito[id]["acumulado"]) - producto.valor)
            else:
                self.eliminar(producto)
            self.guardar_carrito()

    def eliminar(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
