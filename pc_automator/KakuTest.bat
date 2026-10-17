@echo off
title KakuUnlock - Teste Read-Only
color 0A
echo ========================================================
echo         KakuUnlock - Teste de Hardware Real
echo ========================================================
echo.

echo [*] Instalando dependencias do Python (pyusb e rich)...
pip install pyusb rich >nul 2>&1

echo [*] Verificando se o motor mtkclient existe...
if not exist "mtkclient" (
    echo [*] Baixando o motor mtkclient do GitHub...
    git clone https://github.com/bkerler/mtkclient.git
)

echo [*] Instalando dependencias do mtkclient...
cd mtkclient
pip install -r requirements.txt >nul 2>&1
cd ..

echo.
echo ========================================================
echo  TUDO PRONTO! INICIANDO O TESTE...
echo  (Certifique-se de que o celular esta no modo BROM e plugado)
echo ========================================================
echo.

python teste_real_win.py

echo.
echo ========================================================
echo  Teste finalizado. Aperte qualquer tecla para sair.
echo ========================================================
pause >nul
