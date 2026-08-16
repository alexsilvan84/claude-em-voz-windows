@echo off
REM ============================================================
REM  PACOTE DE INSTALACAO DO CLAUDE EM VOZ
REM
REM  Dois cliques aqui e ele instala tudo sozinho, na ordem:
REM
REM      1. Python
REM      2. Git (fornece o "bash" que os ganchos usam)
REM      3. as bibliotecas
REM      4. os reconhecedores de fala
REM      5. os quatro ganchos, com os caminhos deste computador
REM
REM  O CLAUDE CODE NAO E INSTALADO AQUI, de proposito: quem vai
REM  usar este programa ja tem o Claude funcionando, e reinstalar
REM  por cima trocaria a versao dele e poderia estragar o que ja
REM  funcionava. Este arquivo apenas confere que ele existe.
REM
REM  Pula sozinho o que ja estiver instalado, entao pode ser
REM  rodado de novo sem medo.
REM
REM  Tudo sai da pasta Instaladores, aqui do lado: funciona com
REM  a internet desligada.
REM
REM  So DUAS coisas ficam por sua conta no fim, porque vem do
REM  Windows e nao ha como guardar aqui: a voz em portugues e a
REM  liberacao do microfone. Ele avisa quais faltam.
REM ============================================================
setlocal
title Pacote de instalacao do Claude em Voz
cd /d "%~dp0"

set "PROGRAMAS=%~dp0Instaladores\programas"
set "PY="
set "FALTOU="

cls
echo.
echo  ==========================================================
echo                    CLAUDE EM VOZ
echo              pacote de instalacao completo
echo  ==========================================================
echo.
echo   Vou instalar, um por vez:
echo.
echo     1. Python
echo     2. Git
echo     3. as bibliotecas
echo     4. os reconhecedores de fala
echo     5. os quatro ganchos do Claude Code
echo.
echo   O que ja estiver instalado sera pulado.
echo   Leva uns 10 minutos, quase tudo esperando.
echo.
echo   NAO vou mexer no seu Claude Code: voce ja o tem instalado,
echo   e reinstalar por cima poderia trocar a versao dele. Apenas
echo   confiro se ele esta ai.
echo.
echo   Em algum momento o Windows pode pedir permissao numa
echo   janelinha azul: e a instalacao do Git. Responda que sim.
echo.
echo  ----------------------------------------------------------
echo   Para comecar, aperte qualquer tecla.
echo   Para desistir, feche esta janela.
echo  ----------------------------------------------------------
pause >nul

REM ============================================================
REM  1) PYTHON
REM ============================================================
echo.
echo  ==========================================================
echo   [1 de 5] Python
echo  ==========================================================
echo.

REM Nao basta perguntar se existe "python": o Windows vem com um
REM atalho falso que so abre a loja. Por isso perguntamos a versao
REM a ele - o atalho falso nao sabe responder.
python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 (
    set "PY=python"
    echo  Ja esta instalado:
    python --version
    goto :git
)

if not exist "%PROGRAMAS%\python-3.13.1-amd64.exe" (
    echo  Nao achei o instalador do Python na pasta Instaladores.
    echo  Baixe-o em https://www.python.org/downloads/windows/
    echo  e marque "Add python.exe to PATH" ao instalar.
    goto :fim_com_erro
)

echo  Instalando. A tela pode ficar parada por um minuto.
echo.
"%PROGRAMAS%\python-3.13.1-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=1
if errorlevel 1 (
    echo  A instalacao do Python falhou.
    goto :fim_com_erro
)

REM Ele acabou de entrar no caminho de busca, mas esta janela foi
REM aberta antes disso e nao enxerga a mudanca. Entao chamamos o
REM Python pelo endereco, so aqui.
set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not exist "%PY%" (
    echo  Instalei, mas nao achei o python.exe no lugar esperado.
    echo  Feche esta janela, abra de novo e rode este arquivo mais
    echo  uma vez: assim ele ja estara no caminho de busca.
    goto :fim_com_erro
)
echo  Instalado:
"%PY%" --version

:git
REM ============================================================
REM  2) GIT
REM ============================================================
echo.
echo  ==========================================================
echo   [2 de 5] Git
echo  ==========================================================
echo.

git --version >nul 2>&1
if not errorlevel 1 (
    echo  Ja esta instalado:
    git --version
    goto :confere_claude
)

if not exist "%PROGRAMAS%\Git-2.55.0.4-64-bit.exe" (
    echo  Nao achei o instalador do Git na pasta Instaladores.
    echo  Baixe-o em https://git-scm.com/download/win
    goto :fim_com_erro
)

echo  Instalando. O Windows vai pedir permissao: responda que sim.
echo.
"%PROGRAMAS%\Git-2.55.0.4-64-bit.exe" /VERYSILENT /NORESTART /NOCANCEL /SP-
if errorlevel 1 (
    echo  A instalacao do Git falhou ou foi recusada.
    echo  Sem ele os ganchos nao funcionam: o programa nao vai
    echo  ligar sozinho junto com o Claude Code.
    goto :fim_com_erro
)
echo  Instalado.

:confere_claude
REM ============================================================
REM  CONFERENCIA: O CLAUDE CODE (nao instalamos, so olhamos)
REM
REM  Quem usa este programa ja tem o Claude Code instalado e
REM  configurado. Rodar o instalador por cima poderia trocar a
REM  versao dele e quebrar o que ja funcionava - entao aqui so
REM  perguntamos se ele existe.
REM ============================================================
echo.
echo  ----------------------------------------------------------
echo   Conferindo o Claude Code ^(nao vou mexer nele^)
echo  ----------------------------------------------------------
echo.

claude --version >nul 2>&1
if not errorlevel 1 (
    echo  Encontrado:
    claude --version
) else (
    echo  Nao encontrei o comando "claude" nesta janela.
    echo.
    echo  Se voce ja usa o Claude Code, provavelmente e so isto:
    echo  esta janela foi aberta antes de ele entrar no caminho de
    echo  busca. Feche e abra o Prompt de Comando e confira com
    echo      claude --version
    echo.
    echo  Nao vou instalar nem atualizar o Claude por aqui, para
    echo  nao mexer numa instalacao que ja funciona. Sem ele, o
    echo  resto instala normalmente, mas nao havera com quem falar.
    set "FALTOU=1"
)

:bibliotecas
REM ============================================================
REM  3 e 4) BIBLIOTECAS E RECONHECEDORES
REM ============================================================
echo.
echo  ==========================================================
echo   [3 e 4 de 5] Bibliotecas e reconhecedores de fala
echo  ==========================================================

set "SEM_PAUSA=1"
call "%~dp0instalar.bat"
if errorlevel 1 (
    echo  A instalacao das bibliotecas nao terminou.
    goto :fim_com_erro
)

:ganchos
REM ============================================================
REM  5) OS GANCHOS
REM ============================================================
echo.
echo  ==========================================================
echo   [5 de 5] Ganchos do Claude Code
echo  ==========================================================
echo.
echo  Sao eles que ligam e desligam o programa junto com o Claude,
echo  e que fazem as perguntas de escolha serem faladas na hora.
echo.

"%PY%" -X utf8 configurar_ganchos.py
if errorlevel 1 (
    echo.
    echo  Nao consegui escrever os ganchos. O passo a passo para
    echo  faze-lo a mao esta no INSTALAR_DO_ZERO.txt, PASSO 7.
    set "FALTOU=1"
)

REM ============================================================
REM  CONFERENCIA FINAL
REM ============================================================
echo.
echo  ==========================================================
echo   Conferindo
echo  ==========================================================
echo.

REM A bateria de testes vale como prova da instalacao: ela so passa inteira
REM se as bibliotecas estiverem no lugar e o programa carregar. Nao aborta
REM nada - e conferencia, nao requisito.
"%PY%" -X utf8 testes\testar.py >nul 2>&1
if errorlevel 1 (
    echo  [!] A bateria de testes acusou alguma coisa.
    echo      Nao impede de usar, mas vale olhar. Rode testar.bat
    echo      para ver o que foi.
) else (
    echo  [x] Programa conferido: a bateria de testes passou inteira.
)

"%PY%" -X utf8 claude_em_voz.py --vozes 2>nul | findstr /i "portug" >nul
if errorlevel 1 (
    echo  [ ] FALTA A VOZ EM PORTUGUES.
    echo      Configuracoes do Windows ^> Hora e idioma ^>
    echo      Idioma e regiao ^> Adicionar idioma ^>
    echo      Portugues ^(Brasil^) ^> Opcoes de idioma ^> baixar "Fala".
    echo      Depois reinicie o computador.
    set "FALTOU=1"
) else (
    echo  [x] Voz em portugues instalada.
)

echo.
echo  [ ] CONFIRA O MICROFONE, por favor. E o unico item que nao
echo      tenho como testar daqui:
echo      Configuracoes do Windows ^> Privacidade e seguranca ^>
echo      Microfone ^> ligue "Acesso ao microfone" E TAMBEM
echo      "Permitir que aplicativos da area de trabalho acessem
echo      seu microfone".
echo      Essa segunda chave e a que costuma ficar desligada, e
echo      sem ela ele grava silencio sem reclamar de nada.

echo.
echo  ==========================================================
if defined FALTOU (
    echo   QUASE LA. Resolva os itens marcados com [ ] acima.
) else (
    echo   PRONTO. Esta tudo instalado.
)
echo  ==========================================================
echo.
echo   Para experimentar agora:
echo.
echo     1. Feche o Claude Code, se estiver aberto, e abra de
echo        novo. Ele deve falar "Claude em voz iniciado".
echo     2. Pergunte qualquer coisa: a resposta e lida em voz alta.
echo     3. Para ditar, clique na janela do Claude, SEGURE o Ctrl
echo        da esquerda, espere o bipe, fale, e solte a tecla.
echo.
echo   Duvidas: COMO_USAR.txt (o dia a dia) e
echo            PERGUNTAS_E_RESPOSTAS.txt (o porque de cada coisa).
echo.
pause
exit /b 0

:fim_com_erro
echo.
echo  ==========================================================
echo   A instalacao parou aqui. Nada foi desfeito: pode resolver
echo   o que faltou e rodar este arquivo de novo - ele pula o que
echo   ja estiver pronto.
echo.
echo   O passo a passo detalhado, para fazer a mao, esta em
echo   INSTALAR_DO_ZERO.txt.
echo  ==========================================================
echo.
pause
exit /b 1
