

from django.shortcuts import render 


# se crean las vistas
def home(include):
   return render(include, 'app/home.html')

def login(include):
    return render(include, 'app/login.html')
   
def registro(include):
    return render(include, 'app/registro.html')   

def carro(include):
    return render(include, 'app/carro.html') 

def catalogo(include):
    return render(include, 'app/catalogo.html')  

def contactanos(include):
    return render(include, 'app/contactanos.html')  

def ofertas(include):
    return render(include, 'app/ofertas.html')  

def proveedores(include):
    return render(include, 'app/proveedores.html')   


