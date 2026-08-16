# Claude em Voz — Windows

Conversa por voz com o Claude Code, **100% local e offline**. Sem serviço pago,
sem chave de acesso, sem mandar áudio para lugar nenhum.

Um programa só, com as duas metades da conversa:

- **Ouvir** — ele **fala** as respostas novas do Claude em voz alta, inclusive as
  perguntas de múltipla escolha com as opções, **na hora em que aparecem** — e
  não depois que você já escolheu.
- **Falar** — ele **escreve** o que você fala, ao vivo, palavra por palavra,
  enquanto você ainda está falando, como a digitação por voz do celular.

Ele nunca aperta Enter sozinho: a frase fica na linha esperando você ler e
enviar.

> A versão para Linux está em **[claude-em-voz-linux](https://github.com/alexsilvan84/claude-em-voz-linux)**.
> As duas fazem a mesma coisa; o que muda é a camada que encosta no sistema.

## Instalar

Dois cliques em `INSTALAR_TUDO.bat`. Ele instala o Python, o Git, as
bibliotecas, os reconhecedores de fala e os quatro ganchos do Claude Code — e no
fim confere tudo e **diz em voz alta** o que ficou faltando.

**Antes disso, se quiser instalar sem depender da internet**, baixe a pasta
`Instaladores` (1,1 GB) e ponha-a aqui dentro, ao lado do `INSTALAR_TUDO.bat`:

📦 https://drive.google.com/drive/folders/19REkp1EYtnQ42V-NU_FSUJ2GtzuPoOTs

Ela traz o Python, o Git, as 32 bibliotecas e os reconhecedores de fala já
baixados, nas versões exatas em que tudo foi conferido. **Não é obrigatória**:
sem ela o instalador busca tudo na fonte oficial, o que leva alguns minutos a
mais. Ela existe para o dia em que a internet faltar, um link sair do ar, ou uma
versão nova quebrar o que funcionava.

O **Claude Code não é instalado** por aqui, de propósito: quem chega neste
programa já o usa, e passar um instalador por cima trocaria a versão de uma
instalação que funciona.

A receita completa, passo a passo, está em `INSTALAR_DO_ZERO.txt`.

## No dia a dia

Ele liga e desliga sozinho junto com o Claude Code.

Para ditar: clique na janela do Claude, **segure o Ctrl da esquerda**, espere o
bipe, fale, e solte a tecla.

Digite `/voz` na janela do Claude para o menu que liga e desliga cada metade
sem fechar nada, e `/voz 5` para reler a última resposta.

## Se alguma coisa parar

```
diagnostico.bat
```

Confere a voz, o microfone, os reconhecedores, os quatro ganchos e o Claude
Code — e **diz em voz alta** o que encontrou. Ele pega sozinho a falha mais
provável: mover a pasta de lugar deixa os ganchos apontando para o vazio, e
tudo para sem nenhum aviso.

## Os arquivos

| | |
|---|---|
| `COMO_USAR.txt` | o dia a dia |
| `PERGUNTAS_E_RESPOSTAS.txt` | o porquê de cada decisão |
| `INSTALAR_DO_ZERO.txt` | a receita completa de instalação |
| `CLAUDE.md` | a referência técnica, para quem for mexer no código |
| `testar.bat` | a bateria de testes — mais de 200 verificações em 5 s |

## O que não está aqui

A pasta `Instaladores/` (1,1 GB) — ela mora no
[link do Drive](https://drive.google.com/drive/folders/19REkp1EYtnQ42V-NU_FSUJ2GtzuPoOTs)
citado acima. Ficou de fora porque o GitHub recusa arquivo acima de 100 MB, e
três dos que ela guarda passam disso; além do mais, são cópias de programas de
terceiros, não código deste projeto. O `INSTALAR_DO_ZERO.txt` diz de onde vem
cada um.

Também ficam de fora o histórico do que foi ditado e o registro das respostas
lidas: são conteúdo de quem usa, e o programa os refaz sozinho.

## Ambiente conferido

Windows 11 Pro, Python 3.13, voz `Microsoft Maria Desktop - Portuguese(Brazil)`.
