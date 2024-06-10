
from django.shortcuts import render 


# se crean las vistas
def home(include):
   return render(include, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')
   
def registro(request):
    return render(request, 'app/registro.html')   

def carro(request):
    return render(request, 'app/carro.html') 

def catalogo(include):
    return render(include, 'app/catalogo.html')  

def contactanos(request):
    return render(request, 'app/contactanos.html')  

def ofertas(request):
    return render(request, 'app/ofertas.html')  

def proveedores(request):
    return render(request, 'app/proveedores.html')   


