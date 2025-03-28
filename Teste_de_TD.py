import pandas as pd
import tabula
import os
from zipfile import ZipFile, ZIP_DEFLATED

pdf_file = "Anexo_I.pdf"
csv_file = "Rol_de_Procedimentos.csv"
xlsx_file = "Rol_de_Procedimentos.xlsx"
zip_file = "Teste_{Leonardo_Rodrigues}.zip"

tabelas = tabula.read_pdf(pdf_file, pages="3-11")

if tabelas:
    df = pd.concat(tabelas, ignore_index=True)
else:
    print("Nenhuma tabela encontrada no PDF.")
    exit()




substituicoes = {"OD": "Odontológico", "AMB": "Ambulatorial"}
df.replace(substituicoes, inplace=True)

df.to_csv(csv_file, index=False, encoding="utf-8")
df.to_excel(xlsx_file,index=False, engine="openpyxl")

# 2.3 Compactar o CSV em um ZIP
with ZipFile(zip_file, "w", ZIP_DEFLATED) as Zip:
    Zip.write(csv_file, os.path.basename(csv_file))
    Zip.write(xlsx_file,os.path.basename(xlsx_file))


print(f"Arquivo ZIP criado: {zip_file}")
