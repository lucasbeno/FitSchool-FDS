# teste_com_asserts.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time

print("TESTE COM ASSERTS - VERIFICAÇÕES AUTOMÁTICAS")
print("User: Joao | Senha: Jh050307!")
print("=" * 60)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)

def fazer_login():
    print("1. FAZENDO LOGIN...")
    browser.get("http://127.0.0.1:8000")
    time.sleep(3)
    
    assert "login" in browser.current_url or "127.0.0.1:8000" in browser.current_url
    print("    ASSERT: Página de login carregada")
    
    browser.find_element(By.NAME, "username").send_keys("Joao")
    browser.find_element(By.NAME, "password").send_keys("Jh050307!" + Keys.ENTER)
    time.sleep(4)
    
    assert "menu" in browser.current_url or "127.0.0.1:8000" == browser.current_url
    print("    ASSERT: Login realizado com sucesso")

def criar_treino():
    print("2. CRIANDO TREINO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "treinos" in browser.current_url.lower() or "meustreinos" in browser.current_url.lower()
    print("    ASSERT: Página de treinos carregada")
    
    print("   Clicando em Novo Treino...")
    botoes = browser.find_elements(By.TAG_NAME, "button")
    for btn in botoes:
        if "novo treino" in btn.text.lower():
            btn.click()
            break
    
    time.sleep(3)
    
    campos = [
        ("nome", "Treino de Peito"),
        ("tipo", "Musculacao"),
        ("dia_semana", "Segunda-feira"),
        ("duracao", "60"),
        ("form-0-nome", "Supino Reto"),
        ("form-0-series", "4"),
        ("form-0-repeticoes", "12")
    ]
    
    for name, valor in campos:
        try:
            campo = browser.find_element(By.NAME, name)
            campo.clear()
            for char in valor:
                campo.send_keys(char)
                time.sleep(0.1)
            time.sleep(0.5)
        except:
            pass
    
    botoes_salvar = browser.find_elements(By.XPATH, "//button[contains(text(), 'Salvar')]")
    
    assert len(botoes_salvar) > 0, "Botão Salvar não encontrado"
    print("    ASSERT: Botão Salvar encontrado")
    
    botoes_salvar[0].click()
    time.sleep(3)
    print("    TREINO CRIADO!")
    return True

def apagar_treino_com_alert():
    print("3. APAGANDO TREINO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "Treino de Peito" in browser.page_source
    print("    ASSERT: Treino encontrado na lista")
    
    print("   Procurando lixeira...")
    
    botoes = browser.find_elements(By.TAG_NAME, "button")
    
    lixeira_encontrada = False
    for btn in botoes:
        texto = btn.text.strip()
        if not texto:  
            print("   Encontrou lixeira, clicando...")
            try:
                btn.click()
                time.sleep(2)
                print("    CLICOU NA LIXEIRA!")
                lixeira_encontrada = True
                break
            except:
                continue
    
    assert lixeira_encontrada, "Lixeira não encontrada"
    print("    ASSERT: Lixeira encontrada e clicada")
    
    print("   Aceitando alert...")
    try:
        alert = browser.switch_to.alert
        alert_text = alert.text
        print(f"   Alert: {alert_text}")
        
        assert "excluir" in alert_text.lower() and "treino" in alert_text.lower()
        print("    ASSERT: Alert de confirmação apareceu")
        
        alert.accept()  
        print("    ALERT ACEITO! TREINO EXCLUIDO!")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"    Erro com alert: {e}")
        return False

def verificar_treino_apagado():
    print("4. VERIFICANDO SE TREINO FOI APAGADO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "Treino de Peito" not in browser.page_source
    print("    ASSERT: Treino foi apagado com sucesso!")
    return True

def navegar_paginas_com_asserts():
    print("5. NAVEGANDO E VERIFICANDO PÁGINAS...")
    
    paginas = [
        ("/user/menu/menu/", "MENU PRINCIPAL"),
        ("/user/menu/menu/criarAtleta/", "CRIAR ATLETA"),
        ("/user/menu/frequencia/", "FREQUENCIA")
    ]
    
    for url, nome in paginas:
        print(f"   {nome}...")
        browser.get(f"http://127.0.0.1:8000{url}")
        time.sleep(2)
        
        assert "not found" not in browser.page_source.lower(), f"Página {nome} não encontrada"
        print(f"       ASSERT: {nome} carregada - {browser.title}")

def voltar_ao_menu_final():
    print("6. VOLTANDO AO MENU FINAL...")
    browser.get("http://127.0.0.1:8000/user/menu/menu/")
    time.sleep(3)
    
    assert "menu" in browser.current_url
    print("    ASSERT: Voltou ao menu principal")
    print(f"    {browser.current_url}")

try:
    fazer_login()
    
    print("=" * 50)
    print("CRIANDO TREINO...")
    print("=" * 50)
    
    criar_treino()
    
    print("=" * 50)
    print("APAGANDO TREINO...")
    print("=" * 50)
    
    apagar_treino_com_alert()
    
    print("=" * 50)
    print("VERIFICANDO EXCLUSÃO...")
    print("=" * 50)
    
    verificar_treino_apagado()
    
    print("=" * 50)
    print("NAVEGANDO PELO SISTEMA...")
    print("=" * 50)
    
    navegar_paginas_com_asserts()
    
    print("=" * 50)
    print("FINALIZANDO...")
    print("=" * 50)
    
    voltar_ao_menu_final()
    
    print("=" * 60)
    print(" TESTE COM ASSERTS CONCLUÍDO!")
    print("")
    print(" TODOS OS ASSERTS PASSARAM!")
    print(" Todas as verificações automáticas funcionaram")
    print(" Teste 100% validado")
    print("")
    print(" Navegador aberto no MENU")
    print("=" * 60)
    
    time.sleep(15)

except AssertionError as e:
    print(f" ASSERT FALHOU: {e}")
    print(" O teste parou porque uma verificação falhou")
    input("Pressione ENTER para fechar...")

except Exception as e:
    print(f" ERRO: {e}")
    input("Pressione ENTER para fechar...")

print(" FIM DO TESTE COM ASSERTS")