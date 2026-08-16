@echo off
REM ============================================================
REM  Instala as bibliotecas e os reconhecedores de fala.
REM
REM  Quer instalar TUDO de uma vez - Python, Git, bibliotecas,
REM  reconhecedores e ganchos? Use INSTALAR_TUDO.bat. Este arquivo
REM  aqui e so a parte do Python, e serve para reinstalar essa
REM  parte sozinha, sem mexer no resto.
REM
REM  Nenhum dos dois instala o Claude Code: ele ja e seu e fica
REM  como esta.
REM
REM  Ele usa PRIMEIRO o que esta guardado na pasta Instaladores,
REM  aqui do lado. Se algo faltar ali, ai sim busca na internet.
REM  Com a pasta Instaladores completa, isto funciona com o cabo
REM  de rede desligado.
REM
REM  Antes de rodar isto, o Python 3.13 ja precisa estar
REM  instalado, COM a caixinha "Add python.exe to PATH" marcada.
REM  O instalador dele esta em Instaladores\programas.
REM ============================================================
title Instalando as bibliotecas do Claude em Voz
cd /d "%~dp0"

REM Quem chama este arquivo (o INSTALAR_TUDO) ja sabe onde o Python
REM esta e avisa por aqui - importante logo depois de instalar o
REM Python, quando ele ainda nao aparece no caminho de busca.
if not defined PY set "PY=python"

set "GUARDADAS=%~dp0Instaladores\bibliotecas"
set "GUARDADOS=%~dp0Instaladores\modelos_de_voz\huggingface\hub"
set "CACHE=%USERPROFILE%\.cache\huggingface\hub"

echo.
echo  ==========================================================
echo   Bibliotecas e reconhecedores de fala
echo  ==========================================================
echo.

"%PY%" --version >nul 2>&1
if errorlevel 1 (
    echo  O Python nao foi encontrado.
    echo.
    echo  O instalador dele esta guardado aqui:
    echo      Instaladores\programas\python-3.13.1-amd64.exe
    echo.
    echo  Rode-o e MARQUE a caixinha "Add python.exe to PATH" na
    echo  primeira tela. Depois volte e rode este arquivo de novo.
    echo.
    if not defined SEM_PAUSA pause
    exit /b 1
)

echo  Python encontrado:
"%PY%" --version
echo.

echo  ^> Instalando as bibliotecas...
echo.
if exist "%GUARDADAS%" (
    echo  Usando as bibliotecas guardadas na pasta Instaladores.
    echo  Nao precisa de internet.
    echo.
    "%PY%" -m pip install --no-index --find-links "%GUARDADAS%" -r requirements.txt
) else (
    echo  A pasta Instaladores\bibliotecas nao existe aqui.
    echo  Vou buscar na internet.
    echo.
    "%PY%" -m pip install -r requirements.txt
)
if errorlevel 1 (
    echo.
    echo  A instalacao das bibliotecas falhou.
    echo  Se estava buscando na internet, confira a conexao e
    echo  rode este arquivo de novo.
    echo.
    if not defined SEM_PAUSA pause
    exit /b 1
)

echo.
echo  ^> Colocando os reconhecedores de fala no lugar...
echo.
if exist "%GUARDADOS%" (
    if not exist "%CACHE%" mkdir "%CACHE%" >nul 2>&1
    echo  Copiando da pasta Instaladores. Sao 680 MB, um instante.
    xcopy "%GUARDADOS%\*" "%CACHE%\" /E /I /Y /Q >nul
    if errorlevel 1 (
        echo  A copia falhou. Rode este arquivo de novo.
        if not defined SEM_PAUSA pause
        exit /b 1
    )
    echo  Copiados. Nao precisou baixar nada.
) else (
    echo  Nao ha reconhecedores guardados aqui; vou baixar.
    echo  Sao cerca de 600 MB. Pode demorar alguns minutos.
)

echo.
echo  ^> Conferindo que tudo carrega...
echo.
"%PY%" -X utf8 -u claude_em_voz.py --baixar
if errorlevel 1 (
    echo.
    echo  Nao consegui carregar os reconhecedores. Se ele estava
    echo  baixando, confira a internet e rode este arquivo de
    echo  novo: o que ja baixou nao se perde.
    echo.
    if not defined SEM_PAUSA pause
    exit /b 1
)

echo.
echo  Bibliotecas e reconhecedores prontos.

if defined SEM_PAUSA exit /b 0

echo.
echo  ==========================================================
echo   Faltam os passos que dependem do Windows:
echo.
echo    - a voz em portugues e a liberacao do microfone
echo    - os quatro ganchos do Claude Code
echo.
echo   Os dois estao explicados em INSTALAR_DO_ZERO.txt,
echo   passos 6 e 7. Os ganchos tambem saem prontos com:
echo       python configurar_ganchos.py
echo.
echo   Para conferir a voz agora:
echo       python claude_em_voz.py --teste-voz
echo  ==========================================================
echo.
pause
exit /b 0
