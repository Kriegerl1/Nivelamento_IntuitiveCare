import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from zipfile import ZipFile, ZIP_DEFLATED

navegador = webdriver.Firefox()

print("Abrindo o navegador")

navegador.get(
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
)
navegador.maximize_window()


espera = WebDriverWait(navegador, 5)

print("Aguardando ação...")
try:
    overlay = espera.until(EC.element_to_be_clickable((By.TAG_NAME, "div")))
    overlay.click()
    print("Ação concluída!")
except:
    print("Erro ao concluir ação.")

try:
    print("Procurando anexos...")
    link_anexo_I = espera.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Anexo I."))
    )
    link_anexo_II = espera.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Anexo II."))
    )

except:
    print("Erro ao buscar Anexos.")
    navegador.quit()
    exit()

lista_anexos = [("Anexo_I.pdf", link_anexo_I), ("Anexo_II.pdf", link_anexo_II)]

for titulo, link in lista_anexos:
    print("Iniciando download dos anexos...")
    url = link.get_attribute("href")
    resposta = requests.get(url)

    with open(titulo, "wb") as arquivo:
        arquivo.write(resposta.content)
        print(f"Baixando {titulo}!")

navegador.quit()

zip_Titulo = "Anexos.zip"

with ZipFile(zip_Titulo, "w", compression=ZIP_DEFLATED) as Zip:
    for arquivo in lista_anexos:
        print("Compactando anexos...")
        Zip.write(arquivo[0], os.path.basename(arquivo[0]))

    print("Compactação finalizada!")
