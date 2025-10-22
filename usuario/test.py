from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Treino  

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
    
    def test_login_page_loads(self):
        """Testa se a página de login carrega corretamente"""
        response = self.client.get(reverse('login'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login')  
    
    def test_login_success(self):
        """Testa login bem-sucedido"""
        response = self.client.post(reverse('login'), {
            'username': 'Joao',
            'password': 'Jh050307!'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_login_failure(self):
        """Testa login com credenciais erradas"""
        response = self.client.post(reverse('login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid', status_code=200)  

class TreinoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
        self.client.login(username='Joao', password='Jh050307!')
    
    def test_treino_page_access(self):
        """Testa acesso à página de treinos"""
        response = self.client.get(reverse('meus_treinos')) 
        self.assertEqual(response.status_code, 200)
    
    def test_create_treino(self):
        """Testa criação de treino"""
        response = self.client.post(reverse('novo_treino'), {
            'nome': 'Treino Teste',
            'tipo': 'Musculacao',
            'dia_semana': 'Segunda-feira',
            'duracao': 60
        })
        self.assertEqual(response.status_code, 302)

class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Joao',
            password='Jh050307!'
        )
        self.client.login(username='Joao', password='Jh050307!')
    
    def test_menu_page(self):
        """Testa acesso ao menu principal"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
    
    def test_criar_atleta_page(self):
        """Testa acesso à página criar atleta"""
        response = self.client.get(reverse('criar_atleta'))
        self.assertEqual(response.status_code, 200)
    
    def test_frequencia_page(self):
        """Testa acesso à página frequência"""
        response = self.client.get(reverse('frequencia'))
        self.assertEqual(response.status_code, 200)