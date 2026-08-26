import os
import json
from google import genai
from playwright.sync_api import sync_playwright

def extrair_nomes_dietas(texto_bruto):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY não configurada.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Extraia todos os nomes de dietas presentes no texto abaixo. 
    Retorne uma lista JSON de strings contendo apenas os nomes em maiúsculas (ex: ["BRANDA", "BRANDA CONSTIPANTE"]).

    Texto:
    {texto_bruto}
    """

    print("Processando texto com Gemini...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    print("Resposta bruta da IA:", response.text)
    return json.loads(response.text)

def cadastrar_dietas_no_sistema(lista_dietas, url_sistema, usuario, senha):
    """Automatiza o preenchimento no sistema hospitalar."""
    print(f"Total de dietas a cadastrar: {len(lista_dietas)}")

    with sync_playwright() as p:
        # headless=False para acompanhar o preenchimento em tela
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Login no Sistema
        print("Acessando sistema e efetuando login...")
        page.goto(url_sistema)
        page.fill("#email", usuario)      # Ajuste o seletor do usuário
        page.fill("#senha", senha)          # Ajuste o seletor da senha
        page.click("body > div.login-container > div > form > button")                    # Ajuste o botão de entrar
        page.wait_for_load_state("networkidle")

        # 2. ACESSAR O MÓDULO DE NUTRIÇÃO (SELETOR NOVO)
        print("Acessando o módulo de Nutrição...")
        page.click("body > section > div > a.system-link.nutricao")
        page.wait_for_load_state("networkidle")

        # 3. NAVEGAÇÃO NOS MENUS DE CADASTRO
        print("Navegando para Cadastro > Dietas...")
        page.click("#appSidebar > ul > li:nth-child(5) > a > span")
        page.click("#cadastro-submenu > li:nth-child(5) > a")
        page.wait_for_load_state("networkidle")

        # 3. Loop de cadastro de cada dieta
        for indice, nome_dieta in enumerate(lista_dietas, start=1):
            print(f"[{indice}/{len(lista_dietas)}] Cadastrando: {nome_dieta}...")

            # Clica no botão "Nova Dieta"
            page.click("body > main > div > div.toolbar > button")
            page.wait_for_timeout(500)

            # Preenche o Nome da Dieta
            page.fill("#f-dieta-nome", nome_dieta)

            # Seleciona Grupo: Dietas Orais
            page.select_option("#f-dieta-grupo", label="Dietas Orais")

            # Seleciona Categoria: Básica/Oral
            page.select_option("#f-dieta-categoria", label="Básica/Oral")

            # Marca o checkbox "Ativo" (se não vier marcado por padrão)
            checkbox_ativo = page.locator("#f-dieta-ativo")
            if not checkbox_ativo.is_checked():
                checkbox_ativo.check()

            # Preços por refeição: não preenche nada

            # Clica em Salvar
            page.click("#modalConfirmBtn")
            page.wait_for_timeout(1000)  # Aguarda persistência no banco

        print("Todas as dietas foram cadastradas com sucesso!")
        browser.close()

if __name__ == "__main__":
    arquivo_notas = "dietas_lens.txt"

    if not os.path.exists(arquivo_notas):
        print(f"Erro: Arquivo '{arquivo_notas}' não encontrado.")
        exit(1)

    with open(arquivo_notas, "r", encoding="utf-8") as f:
        conteudo_lens = f.read().strip()

    # 1. Extração estruturada
    dietas_extraidas = extrair_nomes_dietas(conteudo_lens)
    print("Dietas identificadas:", dietas_extraidas)

    if not dietas_extraidas:
        print("Erro: Nenhuma dieta foi identificada no arquivo dietas_lens.txt. Verifique o conteúdo do arquivo.")
        exit(1)

    URL_SISTEMA = "http://192.168.0.253/login"
    USUARIO = "yurijaciel2@gmail.com"
    SENHA = "180725"

    cadastrar_dietas_no_sistema(dietas_extraidas, URL_SISTEMA, USUARIO, SENHA)
