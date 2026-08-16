@echo off
REM ============================================================
REM  Versao silenciosa do desligar.bat, usada pelo gancho de fim
REM  de sessao do Claude Code.
REM
REM  Sem echo e sem pause de proposito: um gancho nao pode abrir
REM  janela nem ficar esperando alguem apertar uma tecla.
REM ============================================================
setlocal
set "REGISTRO=%TEMP%\claude_em_voz.pid"
if not exist "%REGISTRO%" exit /b 0
set /p NUMERO=<"%REGISTRO%"
taskkill /PID %NUMERO% /F >nul 2>&1
del "%REGISTRO%" >nul 2>&1
exit /b 0
