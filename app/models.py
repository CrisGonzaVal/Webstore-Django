from django.db import models

# Se crean los modelos (tablas) desde aqui 


class Importadora(models.Model):
    rut_empresa = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
      return self.rut_empresa

class Bodega(models.Model):
    id_bodega = models.AutoField(primary_key=True)
    rut_empresa = models.ForeignKey(Importadora, on_delete=models.CASCADE)

    def __str__(self):
      return self.id_bodega


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
      return self.nombre


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_m = models.CharField(max_length=100)

    def __str__(self):
      return self.nombre_m

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_prod = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.IntegerField(default=0) # valor por defecto 0
    color = models.CharField(max_length=50)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
      return self.nombre_prod

class Inventario(models.Model):
    id_producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    cantidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    estatus = models.CharField(max_length=50)

    def __str__(self):
        return self.id_producto

    

class Dimensiones(models.Model):
    id_producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    alto = models.FloatField()
    largo = models.FloatField()
    ancho = models.FloatField()
    peso = models.FloatField()

class Historial(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    accion = models.TextField()

class Fecha(models.Model):
    id_fecha = models.AutoField(primary_key=True)
    anio = models.IntegerField()
    mes = models.IntegerField()
    dia = models.IntegerField()

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class ComprobantePago(models.Model):
    id_comprobante = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

class TipoPago(models.Model):
    id_n_tarjeta = models.CharField(max_length=50, primary_key=True)
    banco = models.CharField(max_length=100)

class Debito(models.Model):
    id_n_tarjeta = models.OneToOneField(TipoPago, on_delete=models.CASCADE, primary_key=True)

class Credito(models.Model):
    id_n_tarjeta = models.OneToOneField(TipoPago, on_delete=models.CASCADE, primary_key=True)

class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)

class OrdenCompra(models.Model):
    id_orden_compra = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)

class Despacho(models.Model):
    id_despacho = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=50)

class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    calle = models.CharField(max_length=100)
    numero = models.IntegerField()
    id_despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE)

class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Comuna(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=100)
    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

class TipoUsuario(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre    

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    rut = models.CharField(max_length=12, unique=True)
    dv = models.CharField(max_length=1)
    email = models.CharField(max_length=100)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
      return self.nombre + " "+ self.apellido

    
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)


class Cuenta(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    clave_usuario = models.CharField(max_length=100)