@echo off
REM ============================================================
REM  Desliga o Claude em Voz.
REM  Encerra apenas ele, pelo numero anotado quando ligou.
REM  Nenhum outro programa em Python e afetado.
REM ============================================================
setlocal
set "REGISTRO=%TEMP%\claude_em_voz.pid"

if not exist "%REGISTRO%" (
    echo O Claude em Voz nao esta ligado.
    goto fim
)

set /p NUMERO=<"%REGISTRO%"
taskkill /PID %NUMERO% /F >nul 2>&1

if errorlevel 1 (
    echo Ele ja havia sido encerrado.
) else (
    echo Claude em Voz desligado.
)
del "%REGISTRO%" >nul 2>&1

:fim
echo.
pause
