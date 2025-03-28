@echo off
openfiles >nul 2>nul
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)

:: Define a pasta do projeto
set "PROJECT_PATH=%~dp0"

:: Define a pasta do ambiente virtual
set "VENV_PATH=%PROJECT_PATH%Dependencias"

:: Verifica se o venv já existe, se não, cria um novo
if not exist "%VENV_PATH%" (
    echo Criando ambiente virtual...
    python -m venv "%VENV_PATH%"
) else (
:: Ativa o ambiente virtual
start cmd /k "%VENV_PATH%\Scripts\activate.bat && echo Ambiente virtual ativado! && cd /d %PROJECT_PATH% && python -m pip install --upgrade pip && pip install -r requirements.txt && python main.py"
)
:: Pausa para exibir a saída
pause
