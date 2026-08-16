@echo off
REM ============================================================
REM  O MESMO Claude em Voz, mas com a janela aberta, mostrando o
REM  que ele esta lendo e entendendo. Serve para diagnosticar -
REM  no dia a dia use ligar.bat.
REM
REM  ATENCAO: aqui a janela E o programa. Fechar esta janela
REM  desliga tudo.
REM
REM  Nao adianta abrir os dois: o segundo percebe que ja existe
REM  um rodando e encerra sozinho. Desligue o outro antes, com
REM  desligar.bat.
REM ============================================================
title Claude em Voz (janela aberta)
cd /d "%~dp0"
python -X utf8 -u claude_em_voz.py
echo.
echo Encerrado. Pode fechar esta janela.
pause
