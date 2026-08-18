# -*- coding: utf-8 -*-
"""
Roda todos os testes e mostra um resumo.

    python -X utf8 testes\testar.py            todos
    python -X utf8 testes\testar.py limpeza    so os que casarem com a palavra

Sai com codigo zero se tudo passou, e um se alguma coisa falhou - assim ele
serve tanto para olhar na tela quanto para ser chamado por outro programa.
"""

import os
import sys
import time
import traceback
import importlib

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)

import comum                                            # noqa: E402


# A ordem e proposital: os testes que nao dependem de nada vem primeiro, entao
# quando o programa esta muito quebrado a primeira falha ja diz onde olhar.
ARQUIVOS = [
    "teste_limpeza",
    "teste_vocabulario",
    "teste_perguntas",
    "teste_vigia",
    "teste_correcao",
    "teste_ditado",
    "teste_tecla",
    "teste_interruptor",
    "teste_ganchos",
    "teste_diagnostico",
    "teste_som_ocupado",
]


def main():
    filtro = " ".join(sys.argv[1:]).strip().lower()

    print()
    print("=" * 62)
    print(" CLAUDE EM VOZ - testes")
    print("=" * 62)

    total, falhas, comeco = 0, [], time.time()

    for nome in ARQUIVOS:
        if filtro and filtro not in nome:
            continue

        try:
            modulo = importlib.import_module(nome)
        except Exception:
            print("\n  %s" % nome)
            print("    NAO CONSEGUI CARREGAR ESTE ARQUIVO DE TESTE:")
            print(traceback.format_exc())
            falhas.append((nome, "arquivo de teste nao carregou"))
            continue

        p = comum.Provas(getattr(modulo, "TITULO", nome))
        try:
            modulo.rodar(p, comum)
        except Exception:
            p.falhas.append(("o teste estourou no meio", traceback.format_exc()))

        total += p.passaram + len(p.falhas)
        marca = "ok " if not p.falhas else "FALHOU"
        print("\n  [%s] %s  (%d de %d)"
              % (marca, p.titulo, p.passaram, p.passaram + len(p.falhas)))

        for caso, detalhe in p.falhas:
            print("        x %s" % caso)
            for linha in (detalhe or "").splitlines():
                print("          %s" % linha)
            falhas.append((p.titulo, caso))

    print()
    print("=" * 62)
    if falhas:
        print(" %d de %d falharam, em %.1f s:" % (len(falhas), total,
                                                  time.time() - comeco))
        for titulo, caso in falhas:
            print("   - %s: %s" % (titulo, caso))
    else:
        print(" Tudo passou: %d verificacoes em %.1f s."
              % (total, time.time() - comeco))
    print("=" * 62)
    print()

    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
