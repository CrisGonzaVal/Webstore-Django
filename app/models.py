from django.db import models

# Se crean los modelos (tablas) desde aqui 

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
      return self.nombre    


class Producto(models.Model):
    nombre= models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    #imagen = models.ImageField(upload_to="producto", null=True)

    def __str__(self):
      return self.nombre

