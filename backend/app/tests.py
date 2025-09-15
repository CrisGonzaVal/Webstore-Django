from django.test import TestCase

#test basicos para la API

from rest_framework.test import APITestCase
from .models import Producto, Categoria

class ProductoAPITest(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Test')
        
    def test_get_productos(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_producto(self):
        data = {
            'nombre_prod': 'Test Producto',
            'valor': 10000,
            'id_categoria': self.categoria.id_categoria
        }
        response = self.client.post('/api/productos/', data)
        self.assertEqual(response.status_code, 201)
