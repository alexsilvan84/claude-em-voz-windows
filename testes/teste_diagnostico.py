# -*- coding: utf-8 -*-
"""
O diagnostico, e principalmente a conferencia dos ganchos.

A armadilha que ele existe para pegar: mover a pasta do programa de lugar
deixa os quatro ganchos apontando para o vazio, e tudo para de funcionar sem
nenhum aviso na tela. Aqui se confere que ele acusa isso - e, mais dificil,
que NAO acusa quando esta tudo certo.

O falso alarme era real: os quatro ganchos escrevem o caminho de dois jeitos
diferentes, porque tres deles sao lidos pelo bash (barra normal) e o de
desligar e executado pelo cmd (barra invertida dobrada). Comparando sem
uniformizar, o programa dizia "a pasta mudou de lugar" com tudo no lugar.
"""

import os
import sys
import json
import shutil
import tempfile

TITULO = "Diagnostico"

# Os arquivos que os ganchos citam. Eles precisam EXISTIR na pasta fingida,
# senao o proprio diagnostico acusa - com razao - que um gancho aponta para
# arquivo que sumiu, e o caso deixaria de testar o que se queria.
ARQUIVOS_CITADOS = ("claude_em_voz.py", "parar.bat", "comando_de_voz.py")


def montar_pasta_do_programa():
    pasta = tempfile.mkdtemp(prefix="teste_programa_")
    for nome in ARQUIVOS_CITADOS:
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as arquivo:
            arquivo.write("# so para existir\n")
    return pasta


def ganchos_completos(pasta):
    """Um settings.json como o configurar_ganchos.py escreve de verdade."""
    barra = pasta.replace("\\", "/")
    dobrada = pasta.replace("\\", "\\\\")
    python = sys.executable.replace("\\", "/")
    return {
        "hooks": {
            "PreToolUse": [{
                "matcher": "AskUserQuestion",
                "hooks": [{"type": "command", "shell": "bash",
                           "command": '{ cat; echo; } >> "%s/perguntas_pendentes.jsonl"'
                                      % barra}],
            }],
            "SessionStart": [{
                "hooks": [{"type": "command", "shell": "bash",
                           "command": 'nohup "%s" -X utf8 -u '
                                      '"%s/claude_em_voz.py" &' % (python, barra)}],
            }],
            "SessionEnd": [{
                "matcher": "logout|other",
                # Aqui as barras sao invertidas e DOBRADAS: quem executa e o cmd.
                "hooks": [{"type": "command", "shell": "bash",
                           "command": 'cmd //c "%s\\\\parar.bat"' % dobrada}],
            }],
            "UserPromptSubmit": [{
                "hooks": [{"type": "command", "shell": "bash",
                           "command": '"%s" -X utf8 '
                                      '"%s/comando_de_voz.py"' % (python, barra)}],
            }],
        }
    }


def rodar(p, comum):
    voz = comum.carregar("claude_em_voz")

    # ---------- uniformizar caminhos ----------

    igual = voz.caminho_comparavel
    p.igual("barra invertida vira barra normal",
            igual("C:\\Users\\ana"), "c:/users/ana")
    p.igual("barra dobrada tambem",
            igual("C:\\\\Users\\\\ana"), "c:/users/ana")
    p.igual("os dois jeitos ficam iguais no fim",
            igual("C:/Users/ana"), igual("C:\\\\Users\\\\ana"))

    # ---------- a conferencia dos ganchos ----------

    pasta = tempfile.mkdtemp(prefix="teste_diagnostico_")
    PASTA_FINGIDA = montar_pasta_do_programa()
    antes = os.environ.get("CLAUDE_CONFIG_DIR")
    os.environ["CLAUDE_CONFIG_DIR"] = pasta
    settings = os.path.join(pasta, "settings.json")

    def gravar(configuracao, texto=None):
        with open(settings, "w", encoding="utf-8") as arquivo:
            if texto is not None:
                arquivo.write(texto)
            else:
                json.dump(configuracao, arquivo)

    def conferir(pasta_do_programa=PASTA_FINGIDA):
        c = voz.Conferencia()
        with comum.Silencio():
            voz._conferir_ganchos(c, pasta_do_programa)
        return c

    def problemas(c):
        return " ".join(titulo for _, titulo, _d in c.de("problema"))

    try:
        # ---------- tudo certo ----------
        gravar(ganchos_completos(PASTA_FINGIDA))
        c = conferir()
        p.igual("com tudo no lugar, nenhum problema e acusado",
                problemas(c), "")
        p.certo("e ele diz que os quatro estao la",
                any("quatro ganchos" in t for _, t, _d in c.de("ok")))

        # ---------- o caso que dava falso alarme ----------
        # O gancho de desligar usa barras dobradas. Se a comparacao nao
        # uniformizar, este e o caso que acusa mudanca de pasta sem motivo.
        so_o_de_desligar = {"hooks": {
            "SessionEnd": ganchos_completos(PASTA_FINGIDA)["hooks"]["SessionEnd"]}}
        gravar(so_o_de_desligar)
        c = conferir()
        p.nao_contem("barras dobradas nao viram falso alarme de pasta mudada",
                     problemas(c), "OUTRA pasta")

        # ---------- a pasta mudou de lugar ----------
        gravar(ganchos_completos("C:\\Antigo\\ClaudeEmVoz"))
        c = conferir()
        p.contem("pasta mudada e acusada", problemas(c), "OUTRA pasta")
        p.certo("e explica o que fazer",
                any("configurar_ganchos" in (d or "")
                    for _s, _t, d in c.de("problema")))

        # ---------- falta um gancho ----------
        parcial = ganchos_completos(PASTA_FINGIDA)
        del parcial["hooks"]["SessionStart"]
        gravar(parcial)
        c = conferir()
        p.contem("gancho faltando e acusado", problemas(c), "Faltam ganchos")
        p.certo("dizendo o que se perde com ele",
                any("ligar sozinho" in (d or "")
                    for _s, _t, d in c.de("problema")))

        # ---------- nenhum gancho instalado ----------
        gravar({"theme": "dark"})
        c = conferir()
        p.contem("nenhum gancho instalado e acusado",
                 problemas(c), "Faltam ganchos")

        # ---------- arquivo inexistente ----------
        os.remove(settings)
        c = conferir()
        p.contem("sem settings.json ele avisa que nada foi instalado",
                 problemas(c), "nao estao instalados")

        # ---------- arquivo com defeito ----------
        gravar(None, texto='{"hooks": {,}}')
        c = conferir()
        p.contem("settings.json quebrado e acusado, sem estourar",
                 problemas(c), "Nao consegui ler")

        # ---------- o gancho aponta para arquivo que sumiu ----------
        # Acontece ao apagar ou renomear um arquivo do programa sem refazer
        # os ganchos: o caminho continua certo, mas nao ha mais nada la.
        gravar(ganchos_completos(PASTA_FINGIDA))
        guardado = os.path.join(PASTA_FINGIDA, "parar.bat")
        os.remove(guardado)
        c = conferir()
        p.contem("arquivo que sumiu e acusado",
                 problemas(c), "aponta para arquivo que nao existe")
        p.certo("dizendo qual arquivo",
                any("parar.bat" in (d or "") for _s, _t, d in c.de("problema")))
        with open(guardado, "w", encoding="utf-8") as arquivo:
            arquivo.write("# de volta\n")

        # ---------- o comando de barra ----------
        gravar(ganchos_completos(PASTA_FINGIDA))
        c = conferir()
        p.certo("sem o voz.md ele avisa, mas sem alarde",
                any("nao aparece na lista" in t for _, t, _d in c.de("aviso")))
        p.nao_contem("e isso nao conta como problema",
                     problemas(c), "lista")

        os.makedirs(os.path.join(pasta, "commands"), exist_ok=True)
        with open(os.path.join(pasta, "commands", "voz.md"), "w",
                  encoding="utf-8") as arquivo:
            arquivo.write("teste")
        c = conferir()
        p.certo("com o voz.md no lugar, ele reconhece",
                any("/voz aparece" in t for _, t, _d in c.de("ok")))

        # ---------- o resumo falado ----------
        c = voz.Conferencia()
        c.ok("tudo bem")
        p.contem("sem problemas, o resumo e curto",
                 voz._resumo_falado(c), "tudo certo")

        c = voz.Conferencia()
        c.problema("A voz nao respondeu.")
        c.problema("Faltam ganchos: 2 de 4.")
        frase = voz._resumo_falado(c)
        p.contem("com problemas, ele diz quantos", frase, "2 problemas")
        p.contem("e diz quais sao", frase, "A voz nao respondeu.")
        p.contem("mandando olhar a tela para saber o que fazer",
                 frase, "na tela")

        c = voz.Conferencia()
        c.aviso("O programa nao parece estar rodando.")
        frase = voz._resumo_falado(c)
        p.contem("aviso nao e problema", frase, "Nada impedindo")

    finally:
        if antes is None:
            os.environ.pop("CLAUDE_CONFIG_DIR", None)
        else:
            os.environ["CLAUDE_CONFIG_DIR"] = antes
        shutil.rmtree(pasta, ignore_errors=True)
        shutil.rmtree(PASTA_FINGIDA, ignore_errors=True)
