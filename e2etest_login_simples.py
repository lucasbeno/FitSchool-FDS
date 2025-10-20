from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class TestLoginFitSchool(LiveServerTestCase):
    
    def setUp(self):
        print('Criando usuario de teste...')
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@fitschool.com',
            password='admin123'
        )
    
    def test_login_com_sucesso(self):
        print('Iniciando teste de login...')
        browser = webdriver.Chrome()
        
        try:
            # 1. Vai para a página inicial
            browser.get(self.live_server_url)
            time.sleep(2)
            
            # 2. Clica em Entrar
            entrar_btn = browser.find_element(By.XPATH, '//button[contains(text(), "Entrar")]')
            entrar_btn.click()
            time.sleep(2)
            
            # 3. Preenche o formulário
            username_input = browser.find_element(By.NAME, 'username')
            password_input = browser.find_element(By.NAME, 'password')
            
            username_input.send_keys('admin')
            password_input.send_keys('admin123')
            
            # 4. Submete
            submit_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
            submit_button.click()
            time.sleep(3)
            
            # 5. Verifica
            current_url = browser.current_url
            print(f'URL atual: {current_url}')
            
            if 'login' in current_url.lower():
                raise AssertionError('Login falhou - ainda esta na pagina de login')
            
            print('TESTE PASSOU! Login funcionou!')
            
        except Exception as e:
            print(f'ERRO: {e}')
            browser.save_screenshot('erro_teste.png')
            raise
        finally:
            browser.quit()
            print('Navegador fechado')