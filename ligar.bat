@echo off
REM ============================================================
REM  Liga o Claude em Voz, SEM janela nenhuma.
REM  Dois cliques aqui: esta telinha pisca e some, e o programa
REM  fica rodando invisivel.
REM
REM  Ele faz as duas metades da conversa:
REM    - fala as respostas novas do Claude, inclusive as
REM      perguntas de escolha, com as opcoes;
REM    - escreve o que voce falar (segure o Ctrl da esquerda,
REM      espere o bipe, fale, e solte).
REM
REM  Dois bipes subindo avisam que ficou pronto.
REM
REM  Para desligar: dois cliques em desligar.bat
REM  Deu problema? Rode ligar_com_janela.bat, ou leia o arquivo
REM  registro.txt, que guarda tudo o que aconteceu.
REM ============================================================
cd /d "%~dp0"
start "" pythonw.exe -X utf8 claude_em_voz.py
