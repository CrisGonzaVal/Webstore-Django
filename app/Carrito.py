class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.id_producto)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id_producto,
                "nombre": producto.nombre_prod,
                "acumulado": float(producto.valor),  # Convierte Decimal a float para serialización
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += float(producto.valor)
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def disminuir(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito:
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= float(producto.valor)
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            else:
                self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
