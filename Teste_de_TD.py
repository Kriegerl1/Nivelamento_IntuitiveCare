import pandas as pd
import tabula
import os
from zipfile import ZipFile, ZIP_DEFLATED

pdf_file = "Anexo_I.pdf"
csv_file = "Rol_de_Procedimentos.csv"
xlsx_file = "Rol_de_Procedimentos.xlsx"
zip_file = "Teste_{Leonardo_Rodrigues}.zip"


def extrair_tabela_pdf(pdf_file):
    print("Lendo pdf...")
    tabelas = tabula.read_pdf(pdf_file, pages="3-12") 

    dataf = pd.concat(tabelas, ignore_index=True)

    if len(dataf.columns) == 13:
        dataf.columns = [
            "PROCEDIMENTO",
            "RN(alteração)",
            "VIGÊNCIA",
            "OD",
            "AMB",
            "HCO",
            "HSO",
            "REF",
            "PAC",
            "DUT",
            "SUBGRUPO",
            "GRUPO",
            "CAPÍTULO",
        ]

    substituicoes = {"OD": "Odontológico", "AMB": "Ambulatorial"}

    print("Atualizando campos...")
    dataf.replace(substituicoes, inplace=True)

    return dataf

df_final = extrair_tabela_pdf(pdf_file)

if df_final is not None:
    print("Convertendo arquivos...")
    df_final.to_csv(csv_file, index=False, encoding="utf-8")
    df_final.to_excel(xlsx_file, index=False, engine="openpyxl")

    print("Compactando arquivos...")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as Zip:
        Zip.write(csv_file, os.path.basename(csv_file))
        Zip.write(xlsx_file,os.path.basename(xlsx_file))

    print(f"Arquivo ZIP criado: {zip_file}")
