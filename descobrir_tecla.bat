@echo off
REM ============================================================
REM  Descobre o que o seu teclado manda em cada tecla.
REM
REM  Serve para notebook, onde a fileira de cima vem trocada: a
REM  tecla marcada F9 manda um comando da maquina quando apertada
REM  sozinha, e so vira F9 de verdade com o Fn junto.
REM
REM  Aperte a tecla sozinha, depois com o Fn junto, e veja o que
REM  aparece. Depois escreva a receita que ele mostrar na linha
REM  TECLA_DE_FALA, no topo de claude_em_voz.py.
REM
REM  ESC encerra.
REM ============================================================
title Descobrir a tecla
cd /d "%~dp0"
python -X utf8 -u claude_em_voz.py --descobrir-tecla
echo.
pause
