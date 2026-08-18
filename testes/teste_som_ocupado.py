# -*- coding: utf-8 -*-
"""
"O som esta ocupado" nao pode parecer "a voz quebrou".

Isto aconteceu de verdade: o usuario pediu um teste de voz logo depois de uma
resposta comprida, o proprio leitor estava falando e segurando a saida de som,
e o teste despejou um erro de varias linhas terminado num numero. A voz estava
perfeita - mas quem lesse aquilo concluiria o contrario, e iria procurar
defeito onde nao havia.

Aqui se confere que esse caso e reconhecido, que o programa espera a vez em vez
de desistir, e que um erro DE VERDADE continua subindo em vez de ser engolido.
"""

TITULO = "Som ocupado nao e defeito"


class VozQueRecusa(object):
    """
    Uma voz que diz "som ocupado" nas primeiras vezes e depois fala.

    E o comportamento real: o leitor termina a frase dele e libera a saida.
    """

    def __init__(self, recusas, erro):
        self.faltam = recusas
        self.erro = erro
        self.falou = []

    def falar(self, texto, desistir_se=None):
        if self.faltam > 0:
            self.faltam -= 1
            raise self.erro
        self.falou.append(texto)


class ErroDeCom(Exception):
    """Imita o erro que o Windows levanta, que carrega o numero em args."""

    def __init__(self, numero):
        Exception.__init__(self, numero, None, (None, None, None, 0, None))
        self.hresult = numero


def rodar(p, comum):
    voz = comum.carregar("claude_em_voz")

    OCUPADO = voz.SOM_OCUPADO

    # ---------- reconhecer o caso ----------

    p.certo("o numero do som ocupado e reconhecido",
            voz.som_esta_ocupado(ErroDeCom(OCUPADO)))

    # O mesmo numero sem sinal: a biblioteca as vezes o entrega assim.
    p.certo("o mesmo numero sem sinal tambem",
            voz.som_esta_ocupado(ErroDeCom(OCUPADO + 4294967296)))

    p.certo("e reconhecido tambem pelo texto do erro",
            voz.som_esta_ocupado(Exception("erro 0x80045006 no dispositivo")))

    # ---------- o que NAO pode ser confundido ----------

    p.certo("outro erro de voz nao e confundido com som ocupado",
            not voz.som_esta_ocupado(ErroDeCom(-2147201017)))

    p.certo("erro comum nao e confundido",
            not voz.som_esta_ocupado(ValueError("qualquer outra coisa")))

    p.certo("erro sem argumento nenhum nao quebra a conferencia",
            not voz.som_esta_ocupado(Exception()))

    # ---------- esperar a vez ----------

    falsa = VozQueRecusa(recusas=2, erro=ErroDeCom(OCUPADO))
    with comum.Silencio():
        deu_certo = voz.falar_esperando_a_vez(falsa, "oi", tentativas=5,
                                              espera=0.01)
    p.certo("depois de o som liberar, a frase e falada", deu_certo)
    p.igual("e falada uma vez so", falsa.falou, ["oi"])

    # ---------- desistir sem estardalhaco ----------

    teimosa = VozQueRecusa(recusas=99, erro=ErroDeCom(OCUPADO))
    with comum.Silencio() as silencio:
        deu_certo = voz.falar_esperando_a_vez(teimosa, "oi", tentativas=3,
                                              espera=0.01)
    p.certo("som ocupado o tempo todo devolve falso, sem estourar",
            deu_certo is False)
    p.certo("e o programa explica que nao e defeito",
            "NAO e" in silencio.texto or "nao e" in silencio.texto.lower(),
            "disse: %r" % silencio.texto)

    # ---------- um defeito de verdade continua aparecendo ----------

    # Esta e a parte que mantem o conserto honesto: engolir todo erro faria a
    # voz quebrada passar por "som ocupado", e o teste nunca acusaria nada.
    quebrada = VozQueRecusa(recusas=99, erro=ErroDeCom(-2147201001))
    estourou = False
    try:
        with comum.Silencio():
            voz.falar_esperando_a_vez(quebrada, "oi", tentativas=3, espera=0.01)
    except Exception:
        estourou = True
    p.certo("erro de verdade continua subindo, e nao vira espera", estourou)
