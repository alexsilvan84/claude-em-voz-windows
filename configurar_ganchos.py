# -*- coding: utf-8 -*-
"""
=============================================================================
 CONFIGURAR OS GANCHOS DO CLAUDE EM VOZ
=============================================================================

Escreve, no settings.json do Claude Code, os quatro ganchos que fazem o
programa existir sem voce precisar ligar nada:

    SessionStart      liga o Claude em Voz junto com o Claude Code
    SessionEnd        desliga junto
    PreToolUse        entrega as perguntas de multipla escolha na hora,
                      antes de voce escolher - pelo arquivo da conversa
                      elas chegariam tarde demais
    UserPromptSubmit  atende o comando "voz", que liga e desliga cada
                      metade sem fechar nada; qualquer outra linha que
                      voce digite passa intocada

Alem dos ganchos, escreve o comando de barra em

    ~/.claude/commands/voz.md

E ele que faz o  /voz  aparecer na lista quando voce digita a barra: o Claude
Code recusa um comando de barra que nao exista como arquivo, e a recusa
acontece antes de o gancho ver a linha. Sem ele o menu ainda responderia,
mas so digitando  voz  sem barra.

Os caminhos NAO sao chutados: a pasta sai de onde este arquivo esta, e o
pythonw.exe sai do proprio Python que esta rodando isto. E o que permite
instalar em qualquer computador, com qualquer nome de usuario, sem editar
nada a mao.

O que ja existe no settings.json e preservado - tema, permissoes, outros
ganchos seus. So os ganchos DESTE programa sao refeitos. E o arquivo antigo
e copiado para settings.json.copia-de-seguranca antes de qualquer coisa.

Uso:
    python configurar_ganchos.py            escreve os ganchos
    python configurar_ganchos.py --mostrar   so mostra, sem escrever
    python configurar_ganchos.py --remover   tira os ganchos deste programa
=============================================================================
"""

import io
import os
import sys
import json
import shutil

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError, ValueError):
    pass


PASTA = os.path.dirname(os.path.abspath(__file__))


def pasta_do_claude():
    """
    A pasta de configuracao do Claude Code.

    CLAUDE_CONFIG_DIR ganha da pasta padrao, porque quem a define esta
    justamente dizendo que mudou o lugar.
    """
    config = os.environ.get("CLAUDE_CONFIG_DIR")
    if config:
        return config
    perfil = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    return os.path.join(perfil, ".claude")


def caminho_do_settings():
    """Onde o Claude Code guarda as configuracoes do usuario."""
    return os.path.join(pasta_do_claude(), "settings.json")


def caminho_do_comando_de_barra():
    """
    O arquivo que faz o /voz existir na lista de comandos do Claude Code.

    Fica na pasta do usuario, e nao na do projeto, porque o programa e um so
    para a maquina inteira: o menu tem que responder em qualquer pasta onde
    voce abrir o Claude Code.
    """
    return os.path.join(pasta_do_claude(), "commands", "voz.md")


def achar_pythonw():
    """
    O irmao sem janela do Python que esta rodando isto.

    Tem que ser pythonw.exe, e nao python.exe: e o "w" que evita uma janela
    preta abrindo a cada sessao do Claude Code. Se por algum motivo ele nao
    existir, o python.exe comum serve - com janela, mas funcionando.
    """
    pasta = os.path.dirname(sys.executable)
    candidato = os.path.join(pasta, "pythonw.exe")
    if os.path.isfile(candidato):
        return candidato
    return sys.executable


def achar_python():
    """
    O Python COM janela de texto, irmao do de cima.

    Nao basta usar o que esta rodando isto: se alguem chamar este arquivo
    pelo pythonw, o gancho do menu herdaria um Python sem entrada nem saida
    de texto, e o menu nunca apareceria.
    """
    pasta = os.path.dirname(sys.executable)
    candidato = os.path.join(pasta, "python.exe")
    if os.path.isfile(candidato):
        return candidato
    return sys.executable


def barras_normais(caminho):
    """Caminho como o bash gosta de ler."""
    return caminho.replace("\\", "/")


def barras_dobradas(caminho):
    """
    Caminho como o cmd precisa receber DEPOIS de passar pelo bash.

    O gancho roda com shell bash, e o bash come uma barra invertida de cada
    par. Entregando as barras dobradas, o cmd recebe o caminho inteiro.
    """
    return caminho.replace("\\", "\\\\")


def montar_ganchos():
    programa = os.path.join(PASTA, "claude_em_voz.py")
    registro = os.path.join(PASTA, "registro.txt")
    perguntas = os.path.join(PASTA, "perguntas_pendentes.jsonl")
    parar = os.path.join(PASTA, "parar.bat")
    menu = os.path.join(PASTA, "comando_de_voz.py")
    pythonw = achar_pythonw()

    # Aqui e python.exe, e nao o pythonw: este gancho conversa com o Claude
    # Code por texto - recebe a sua linha e devolve o menu -, e o pythonw
    # nasce sem essas vias de entrada e saida.
    menu_de_voz = ('"%s" -X utf8 "%s"'
                   % (barras_normais(achar_python()), barras_normais(menu)))

    ligar = (
        'nohup "%s" -X utf8 -u "%s" > "%s" 2>&1 &'
        % (barras_normais(pythonw), barras_normais(programa),
           barras_normais(registro))
    )
    guardar_pergunta = (
        '{ cat; echo; } >> "%s"' % barras_normais(perguntas)
    )
    desligar = 'cmd //c "%s"' % barras_dobradas(parar)

    return {
        "PreToolUse": [{
            "matcher": "AskUserQuestion",
            "hooks": [{
                "type": "command",
                "command": guardar_pergunta,
                "shell": "bash",
                "timeout": 5,
            }],
        }],
        "SessionStart": [{
            "hooks": [{
                "type": "command",
                "command": ligar,
                "shell": "bash",
                "async": True,
                "timeout": 15,
                "statusMessage": "Ligando o Claude em Voz...",
            }],
        }],
        # De proposito SEM "clear" e sem "resume": nesses dois a sessao
        # termina e recomeca em seguida, e desligar ali arriscaria a partida
        # seguinte esbarrar no processo ainda morrendo e ficar sem leitor.
        "SessionEnd": [{
            "matcher": "logout|prompt_input_exit|bypass_permissions_disabled|other",
            "hooks": [{
                "type": "command",
                "command": desligar,
                "shell": "bash",
                "timeout": 10,
                "statusMessage": "Desligando o Claude em Voz...",
            }],
        }],
        # Sem statusMessage de proposito: este dispara a CADA linha que voce
        # digita, e um recado na tela toda vez seria um estorvo. Ele so
        # aparece quando a linha e mesmo um comando da voz.
        "UserPromptSubmit": [{
            "hooks": [{
                "type": "command",
                "command": menu_de_voz,
                "shell": "bash",
                "timeout": 10,
            }],
        }],
    }


# ---------------------------------------------------------------------------
#  O comando de barra
# ---------------------------------------------------------------------------
# Digitar  voz  ja funcionava: o gancho UserPromptSubmit reconhece a linha e a
# engole antes de virar pergunta. Mas o Claude Code so oferece na lista - e so
# aceita - os comandos de barra que existem como arquivo. Sem este arquivo,
# um  /voz  seria recusado como comando desconhecido antes de o gancho ver a
# linha, e a barra e justamente o jeito que o usuario espera.
#
# O arquivo tambem serve de rede: se algum dia o gancho nao pegar a linha, o
# proprio comando chama o comando_de_voz.py e o menu aparece do mesmo jeito.

MODELO_DO_COMANDO = """---
description: Menu da voz - liga e desliga a leitura e o ditado
argument-hint: [1 a 5]
allowed-tools: Bash
---

!`{chamada} $ARGUMENTS`

O texto acima ja apareceu na tela do usuario, inteiro. Nao repita, nao resuma
e nao comente nada sobre ele. Responda somente com um ponto final.
"""


def texto_do_comando_de_barra():
    return MODELO_DO_COMANDO.format(
        chamada='"%s" -X utf8 "%s"'
                % (barras_normais(achar_python()),
                   barras_normais(os.path.join(PASTA, "comando_de_voz.py"))))


def escrever_comando_de_barra():
    """Cria o /voz. Devolve o caminho, ou None se nao deu."""
    caminho = caminho_do_comando_de_barra()
    try:
        pasta = os.path.dirname(caminho)
        if pasta and not os.path.isdir(pasta):
            os.makedirs(pasta)
        with io.open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_do_comando_de_barra())
        return caminho
    except OSError as erro:
        print("Nao consegui criar o comando /voz:", erro)
        return None


def remover_comando_de_barra():
    """
    Apaga o /voz - mas so se for mesmo o nosso.

    A conferencia do conteudo existe porque o nome "voz.md" e comum demais:
    se o usuario tiver um comando proprio com esse nome, apagar seria estragar
    trabalho alheio.
    """
    caminho = caminho_do_comando_de_barra()
    if not os.path.isfile(caminho):
        return False
    try:
        with io.open(caminho, "r", encoding="utf-8-sig") as arquivo:
            if "comando_de_voz.py" not in arquivo.read():
                print("Ha um voz.md que nao e deste programa. Nao mexi nele.")
                return False
        os.remove(caminho)
        return True
    except OSError:
        return False


MARCAS = ("claude_em_voz", "perguntas_pendentes", "parar.bat",
          "comando_de_voz")


def e_nosso(entrada):
    """Reconhece um gancho deste programa, para poder refaze-lo sem duplicar."""
    try:
        texto = json.dumps(entrada, ensure_ascii=False).lower()
    except (TypeError, ValueError):
        return False
    return any(marca in texto for marca in MARCAS)


def limpar_os_nossos(configuracao):
    """
    Tira os ganchos deste programa e devolve quantos saiu.

    Isto e o que torna a instalacao repetivel: rodar duas vezes nao empilha
    dois leitores, e mudar a pasta de lugar nao deixa o gancho velho para
    tras apontando para o vazio.
    """
    ganchos = configuracao.get("hooks")
    if not isinstance(ganchos, dict):
        return 0

    removidos = 0
    for evento in list(ganchos.keys()):
        lista = ganchos.get(evento)
        if not isinstance(lista, list):
            continue
        sobraram = [item for item in lista if not e_nosso(item)]
        removidos += len(lista) - len(sobraram)
        if sobraram:
            ganchos[evento] = sobraram
        else:
            del ganchos[evento]

    if not ganchos:
        configuracao.pop("hooks", None)
    return removidos


def ler(caminho):
    """
    Le o settings.json que ja existe.

    Devolve (configuracao, deu_certo). Se o arquivo estiver corrompido, NAO
    inventamos um novo por cima: perder as permissoes e o tema do usuario
    por causa de uma virgula fora do lugar seria bem pior do que parar e
    avisar.
    """
    if not os.path.isfile(caminho):
        return {}, True
    # utf-8-sig, e nao utf-8: o Bloco de Notas do Windows carimba uma marca
    # invisivel no comeco do arquivo ao salvar. Ela nao atrapalha ninguem,
    # mas faz a leitura comum falhar dizendo que o arquivo esta corrompido -
    # e ai o usuario acharia que perdeu as configuracoes por ter aberto o
    # arquivo para olhar. O "sig" engole essa marca.
    try:
        with io.open(caminho, "r", encoding="utf-8-sig") as arquivo:
            texto = arquivo.read().strip()
    except OSError as erro:
        print("Nao consegui ler o settings.json:", erro)
        return None, False
    if not texto:
        return {}, True
    try:
        dados = json.loads(texto)
    except ValueError as erro:
        print("O settings.json existe, mas esta com defeito de escrita:")
        print("   ", erro)
        print("Nada foi alterado. Abra o arquivo, conserte, e rode de novo:")
        print("   ", caminho)
        return None, False
    if not isinstance(dados, dict):
        print("O settings.json nao tem o formato esperado. Nada foi alterado.")
        return None, False
    return dados, True


def guardar_copia(caminho):
    if not os.path.isfile(caminho):
        return None
    copia = caminho + ".copia-de-seguranca"
    try:
        shutil.copy2(caminho, copia)
        return copia
    except OSError:
        return None


def escrever(caminho, configuracao):
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.isdir(pasta):
        os.makedirs(pasta)
    texto = json.dumps(configuracao, indent=2, ensure_ascii=False)
    with io.open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")


def main():
    caminho = caminho_do_settings()
    ganchos = montar_ganchos()

    if "--mostrar" in sys.argv:
        print("Arquivo de configuracoes:")
        print("   ", caminho)
        print()
        print("Ganchos que seriam escritos:")
        print(json.dumps({"hooks": ganchos}, indent=2, ensure_ascii=False))
        print()
        print("Comando de barra que seria criado:")
        print("   ", caminho_do_comando_de_barra())
        print(texto_do_comando_de_barra())
        return 0

    configuracao, deu_certo = ler(caminho)
    if not deu_certo:
        return 1

    copia = guardar_copia(caminho)
    if copia:
        print("Copia de seguranca do arquivo antigo:")
        print("   ", os.path.basename(copia))

    removidos = limpar_os_nossos(configuracao)
    if removidos:
        print("Ganchos antigos deste programa retirados:", removidos)

    if "--remover" in sys.argv:
        escrever(caminho, configuracao)
        if remover_comando_de_barra():
            print("Comando /voz retirado.")
        print("Pronto. O Claude em Voz nao liga mais sozinho.")
        print("Para ligar na mao, use ligar.bat.")
        return 0

    existentes = configuracao.get("hooks")
    if not isinstance(existentes, dict):
        existentes = {}
    for evento, lista in ganchos.items():
        existentes.setdefault(evento, [])
        existentes[evento] = list(existentes[evento]) + list(lista)
    configuracao["hooks"] = existentes

    escrever(caminho, configuracao)

    comando = escrever_comando_de_barra()

    print("Ganchos instalados em:")
    print("   ", caminho)
    if comando:
        print()
        print("Comando /voz criado em:")
        print("   ", comando)
    print()
    print("Apontando para:")
    print("    programa:", os.path.join(PASTA, "claude_em_voz.py"))
    print("    Python:  ", achar_pythonw())
    print()
    print("Feche o Claude Code e abra de novo: ele nem sempre recarrega as")
    print("configuracoes na sessao que ja esta rodando.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
