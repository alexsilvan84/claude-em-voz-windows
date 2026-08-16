@echo off
REM ============================================================
REM  Roda a bateria de testes do Claude em Voz.
REM
REM  Dois cliques aqui depois de mexer em qualquer coisa do
REM  programa. Em poucos segundos ele confere tudo o que ja deu
REM  errado alguma vez: leitura de codigo em voz alta, historico
REM  relido, texto apagado da tela por engano, a tecla brigando
REM  com Ctrl+C, e a instalacao estragando o settings.json.
REM
REM  Nao precisa de microfone, nem de caixa de som, nem de
REM  internet, e nao encosta no seu settings.json nem no
REM  interruptor: tudo o que ele escreve vai para pasta
REM  temporaria.
REM
REM  Pode rodar com o programa ligado.
REM ============================================================
title Testes do Claude em Voz
cd /d "%~dp0"

python -X utf8 -u testes\testar.py %*
set "RESULTADO=%ERRORLEVEL%"

if not "%RESULTADO%"=="0" (
    echo.
    echo  ----------------------------------------------------------
    echo   Alguma coisa falhou. Cada linha acima marcada com x diz o
    echo   que era esperado e o que aconteceu. Se voce acabou de
    echo   mexer no programa, o defeito costuma estar ai.
    echo  ----------------------------------------------------------
)

echo.
pause
exit /b %RESULTADO%
