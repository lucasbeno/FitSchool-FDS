from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
    
    def test_login_page_loads(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_login_success(self):
        user = authenticate(username='Joao', password='Jh050307!')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'Joao')
    
    def test_login_failure(self):
        user = authenticate(username='wrong', password='wrong')
        self.assertIsNone(user)

class TreinoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
        login_success = self.client.login(username='Joao', password='Jh050307!')
        self.assertTrue(login_success)
    
    def test_treino_page_access(self):
        response = self.client.get('/user/menu/meusTreinos/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_treino_page(self):
        response = self.client.get('/user/menu/meusTreinos/')
        self.assertEqual(response.status_code, 200)

class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
        login_success = self.client.login(username='Joao', password='Jh050307!')
        self.assertTrue(login_success)
    
    def test_menu_page(self):
        response = self.client.get('/user/menu/menu/')
        self.assertEqual(response.status_code, 200)
    
    def test_criar_atleta_page(self):
        response = self.client.get('/user/menu/menu/criarAtleta/')
        self.assertEqual(response.status_code, 200)
    
    def test_frequencia_page(self):
        response = self.client.get('/user/menu/frequencia/')
        self.assertEqual(response.status_code, 200)