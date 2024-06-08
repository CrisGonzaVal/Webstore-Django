
from django.shortcuts import render 
from.models import Producto

# se crean las vistas
def home(request):
   productos=Producto.objects.all()
   data={
       'productos': productos
   }
   return render(request, 'app/home.html', data)

def login(request):
    return render(request, 'app/login.html')
   
def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    return render(request, 'app/carro.html') 

def catalogo(request):
    return render(request, 'app/catalogo.html')  

def contactanos(request):
    return render(request, 'app/contactanos.html')  

def ofertas(request):
    return render(request, 'app/ofertas.html')  

def proveedores(request):
    return render(request, 'app/proveedores.html')   


