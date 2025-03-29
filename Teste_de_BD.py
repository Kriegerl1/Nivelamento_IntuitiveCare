import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import time

navegador = webdriver.Firefox()

espera = WebDriverWait(navegador, 5)

navegador.get("https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/")

navegador.maximize_window()

data = time.localtime().tm_year

arquivos_ = {}

ultimos_dois_anos = [str(data - 1), str(data - 2)]

try:
    for ano in ultimos_dois_anos:

        print(f"Buscando a pasta de {ano}...")
        pasta_selecionada = espera.until(
            EC.element_to_be_clickable((By.LINK_TEXT, f"{ano}/"))
        )
        pasta_selecionada.click()

        links = navegador.find_elements(By.TAG_NAME, "a")

        print("Buscando todos os zip disponíveis...")
        arquivos_zip = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href")
            and link.get_attribute("href").endswith(".zip")
        ]

        arquivos_[ano] = arquivos_zip

        for link in arquivos_[ano]:
            nome_arquivo = os.path.basename(link)

            resposta = requests.get(link, stream=True)
            with open(nome_arquivo, "wb") as arquivo:
                arquivo.write(resposta.content)
                print(f"Baixando arquivo: {nome_arquivo}")
            navegador.back()
except Exception as err:
    print("Erro ao baixar arquivos: {err}")

navegador.get(
    "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
)

try:
    print(f"Buscando a pasta de Dados Cadastrais...")
    pasta_selecionada = espera.until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f"dicionario_de_dados_.."))
    )
    link_dados = pasta_selecionada.get_attribute("href")

    nome_arquivo = os.path.basename(link_dados)

    resposta = requests.get(link_dados)

    with open(nome_arquivo, "wb") as arquivo:
        arquivo.write(resposta.content)
        print(f"Baixando arquivo: {nome_arquivo}")

    print("Convertendo para .ods ...")
    df = pd.read_excel(nome_arquivo, engine="odf")
    csv_path = nome_arquivo.replace(".odc", ".csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print("Arquivo convertido!")


except Exception as err:
    print(f"Erro ao baixar dados cadastrais: {err}")

finally:
    navegador.quit()
