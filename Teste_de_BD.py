import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

navegador = webdriver.Firefox()
espera = WebDriverWait(navegador, 5)
navegador.get("https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/")

navegador.maximize_window()

data = time.localtime().tm_year

print(data)

arquivos_ = {}

Ultimos_dois_anos = [str(data - 1), str(data - 2)]

print(Ultimos_dois_anos)

try:
    for ano in Ultimos_dois_anos:
        print(f"Procurando o ano de {ano}")
        pasta_selecionada = espera.until(
            EC.element_to_be_clickable((By.LINK_TEXT, f"{ano}/"))
        )
        pasta_selecionada.click()

        links = navegador.find_elements(By.TAG_NAME, "a")

        arquivos_zip = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href")
            and link.get_attribute("href").endswith(".zip")
        ]

        arquivos_[ano] = arquivos_zip

        for link in arquivos_[ano]:
            nome_arquivo =  os.path.basename(link)

            resposta = requests.get(link, stream=True)
            with open(nome_arquivo, "wb") as arquivo:
                arquivo.write(resposta.content)

except:
    print("Erro")

finally:
    navegador.quit()