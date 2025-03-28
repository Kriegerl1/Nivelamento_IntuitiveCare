@echo off
:: Solicita confirmação do usuário para remover a venv
set /p CONFIRM="Tem certeza que deseja remover a venv (Dependencias)? (S/N): "

if /i "%CONFIRM%" NEQ "S" (
    echo Remoção cancelada.
    exit /b
)

:: Define o caminho da venv a ser removida
set "VENV_PATH=%~dp0\Dependencias"

:: Verifica se a venv existe
if exist "%VENV_PATH%" (
    echo Removendo venv em: %VENV_PATH%
    rmdir /s /q "%VENV_PATH%"  :: Remove a pasta da venv e todo o conteúdo
    echo Venv removida com sucesso!
) else (
    echo A venv não foi encontrada no diretório atual.
)

pause
