@echo off
REM ============================================================
REM  O programa conferindo a si mesmo, e DIZENDO o resultado em
REM  voz alta.
REM
REM  Dois cliques aqui quando alguma coisa parar de funcionar.
REM  Ele confere, um por um: a voz em portugues, o microfone, os
REM  dois reconhecedores, os quatro ganchos, o Claude Code, e se
REM  o programa esta no ar agora.
REM
REM  No fim ele FALA quantos problemas achou e quais sao. O que
REM  fazer em cada caso fica escrito nesta tela.
REM
REM  Pode rodar com o programa ligado - alias, e o melhor jeito.
REM  Leva uns cinco segundos, quase tudo carregando os
REM  reconhecedores.
REM ============================================================
title Diagnostico do Claude em Voz
cd /d "%~dp0"

python -X utf8 -u claude_em_voz.py --diagnostico
set "RESULTADO=%ERRORLEVEL%"

if "%RESULTADO%"=="0" (
    echo.
    echo   Nada a fazer. Se mesmo assim algo parece errado, o
    echo   registro.txt conta o que aconteceu na ultima partida.
)

echo.
pause
exit /b %RESULTADO%
