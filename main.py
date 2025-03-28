import os

scripts = ["Teste_de_WS.py", "Teste_de_TD.py", "Teste_de_BD.py"]

DIRETORIO_BASE = os.path.dirname(os.path.realpath(__file__))

for script in scripts:
    caminho = os.path.join(DIRETORIO_BASE, script)
    print(f"Executando {script} em {caminho}...")
    os.system(f"python {caminho}")
    print(f"{script} finalizado!\n")

print("Todos os scripts foram executados!")
