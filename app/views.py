from django.shortcuts import render

# se crean las vistas

def home(include):
    return render(include, 'app/home.html')

def contacto(include):
    return render(include, 'app/contacto.html')
   
def galeria(include):
    return render(include, 'app/galeria.html')   
