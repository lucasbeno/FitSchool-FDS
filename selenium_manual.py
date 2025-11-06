from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

print("TESTE COM ASSERTS - VERIFICAÇÕES AUTOMÁTICAS")
print("User: Joao | Senha: Jh050307!")
print("=" * 60)

# ✅ Configurações corretas para rodar no GitHub Actions (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Roda sem abrir janela
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")

browser = webdriver.Chrome(options=chrome_options)

# =======================================================
# FUNÇÕES DE TESTE AUTOMATIZADO
# =======================================================

def fazer_login():
    print("1. FAZENDO LOGIN...")
    browser.get("http://127.0.0.1:8000")
    time.sleep(3)
    
    assert "login" in browser.current_url or "127.0.0.1:8000" in browser.current_url
    print("    ✅ ASSERT: Página de login carregada")
    
    browser.find_element(By.NAME, "username").send_keys("Joao")
    browser.find_element(By.NAME, "password").send_keys("Jh050307!" + Keys.ENTER)
    time.sleep(4)
    
    assert "menu" in browser.current_url or "127.0.0.1:8000" == browser.current_url
    print("    ✅ ASSERT: Login realizado com sucesso")

def criar_treino():
    print("2. CRIANDO TREINO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "treinos" in browser.current_url.lower() or "meustreinos" in browser.current_url.lower()
    print("    ✅ ASSERT: Página de treinos carregada")
    
    print("   Clicando em Novo Treino...")
    botoes = browser.find_elements(By.TAG_NAME, "button")
    for btn in botoes:
        if "novo treino" in btn.text.lower():
            btn.click()
            break
    
    time.sleep(3)
    
    campos = [
        ("nome", "Treino Com Assert"),
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
            campo.send_keys(valor)
            time.sleep(0.3)
        except Exception:
            pass
    
    botoes_salvar = browser.find_elements(By.XPATH, "//button[contains(text(), 'Salvar')]")
    assert len(botoes_salvar) > 0, "Botão Salvar não encontrado"
    print("    ✅ ASSERT: Botão Salvar encontrado")
    
    botoes_salvar[0].click()
    time.sleep(3)
    print("    ✅ TREINO CRIADO!")

def apagar_treino_com_alert():
    print("3. APAGANDO TREINO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "Treino Com Assert" in browser.page_source
    print("    ✅ ASSERT: Treino encontrado na lista")
    
    botoes = browser.find_elements(By.TAG_NAME, "button")
    lixeira_encontrada = False
    
    for btn in botoes:
        if btn.text.strip() == "":
            try:
                btn.click()
                time.sleep(2)
                lixeira_encontrada = True
                print("    🗑️ Clicou na lixeira!")
                break
            except Exception:
                continue
    
    assert lixeira_encontrada, "Lixeira não encontrada"
    print("    ✅ ASSERT: Lixeira encontrada e clicada")
    
    try:
        alert = browser.switch_to.alert
        alert_text = alert.text
        print(f"   Alert: {alert_text}")
        
        assert "excluir" in alert_text.lower() and "treino" in alert_text.lower()
        print("    ✅ ASSERT: Alert de confirmação apareceu")
        
        alert.accept()
        print("    ✅ ALERT ACEITO! TREINO EXCLUÍDO!")
        time.sleep(2)
    except Exception as e:
        print(f"    ⚠️ Erro com alert: {e}")

def verificar_treino_apagado():
    print("4. VERIFICANDO SE TREINO FOI APAGADO...")
    browser.get("http://127.0.0.1:8000/user/menu/meusTreinos/")
    time.sleep(3)
    
    assert "Treino Com Assert" not in browser.page_source
    print("    ✅ ASSERT: Treino foi apagado com sucesso!")

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
        print(f"       ✅ ASSERT: {nome} carregada")

def voltar_ao_menu_final():
    print("6. VOLTANDO AO MENU FINAL...")
    browser.get("http://127.0.0.1:8000/user/menu/menu/")
    time.sleep(3)
    
    assert "menu" in browser.current_url
    print("    ✅ ASSERT: Voltou ao menu principal")

# =======================================================
# EXECUÇÃO SEQUENCIAL DO TESTE
# =======================================================
try:
    fazer_login()
    criar_treino()
    apagar_treino_com_alert()
    verificar_treino_apagado()
    navegar_paginas_com_asserts()
    voltar_ao_menu_final()
    
    print("=" * 60)
    print("✅ TESTE COM ASSERTS CONCLUÍDO!")
    print("💯 Todos os asserts passaram com sucesso!")
    print("=" * 60)

except AssertionError as e:
    print(f"❌ ASSERT FALHOU: {e}")
    browser.save_screenshot("assert_fail.png")
    raise SystemExit(1)

except Exception as e:
    print(f"⚠️ ERRO GERAL: {e}")
    browser.save_screenshot("error_fail.png")
    raise SystemExit(1)

finally:
    browser.quit()
