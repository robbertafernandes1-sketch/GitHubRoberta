---
name: grill-me
description: Entrevista a usuária sobre um plano, uma pergunta por vez, com opções clicáveis e a recomendação do Claude como primeira opção, e no fim salva as decisões em docs/fase-1-grill-me.md. Use quando a usuária pedir "grill me", "me entrevista", "me sabatina", "questiona meu plano", "me faça perguntas sobre o plano" ou invocar /grill-me.
---

# Grill Me

Entreviste a usuária sobre um plano até que todas as decisões importantes estejam tomadas, e registre o resultado em `docs/fase-1-grill-me.md`.

## Antes de perguntar: investigue

1. Identifique o plano. Se a usuária passou o plano (texto, arquivo ou argumento da skill), use-o. Se não houver plano nenhum, a primeira pergunta é qual plano vamos discutir.
2. Leia os arquivos do projeto que têm relação com o plano (README, CLAUDE.md, `docs/`, código, configs, `docs/fase-1-grill-me.md` se já existir).
3. **Não pergunte nada que dê para descobrir lendo os arquivos.** Se a resposta está no repositório, use-a e apenas mencione o que encontrou. Pergunte somente o que depende de vontade, prioridade, gosto ou contexto que só a usuária tem.
4. Monte mentalmente a lista de decisões em aberto, da mais fundamental (que muda as outras) para a mais detalhada.

## Como perguntar

- **Uma pergunta por vez.** Use a ferramenta `AskUserQuestion` com exatamente uma pergunta por chamada e espere a resposta antes da próxima.
- **Sempre com opções para clicar**: 2 a 4 opções concretas e mutuamente exclusivas, cada uma com uma descrição curta da consequência ou do trade-off. Não inclua uma opção "Outro" — a ferramenta já oferece campo livre.
- **Sua recomendação é sempre a primeira opção**, com " (Recomendado)" no fim do rótulo. Baseie a recomendação no que você leu do projeto e no que já foi decidido.
- Use `multiSelect: true` só quando as escolhas realmente não se excluem.
- Escreva as perguntas em português, claras e autocontidas, com um `header` curto (até 12 caracteres).
- Adapte a sequência às respostas: uma decisão pode eliminar perguntas ou abrir novas. Não repita perguntas já respondidas.
- Seja exigente: aponte riscos, lacunas e contradições do plano por meio das próprias perguntas e opções.
- Pare quando não houver mais decisões relevantes em aberto (normalmente entre 5 e 15 perguntas). Se a usuária pedir para parar, pare e salve o que já foi decidido.

## No fim: salve as decisões

Crie `docs/` se não existir e escreva (ou atualize, preservando o que já estiver lá) `docs/fase-1-grill-me.md` neste formato:

```markdown
# Fase 1 — Grill Me

**Data:** AAAA-MM-DD
**Plano:** resumo do plano em uma ou duas frases

## Decisões

| # | Pergunta | Decisão | Recomendação do Claude |
|---|----------|---------|------------------------|
| 1 | ... | ... | ... (seguida / não seguida) |

## Fatos encontrados nos arquivos

- O que foi descoberto lendo o projeto, em vez de perguntado (com o caminho do arquivo).

## Pontos em aberto

- O que ficou sem decisão ou precisa de investigação depois.

## Próximos passos

- Ações concretas que decorrem das decisões.
```

Depois de salvar, mostre à usuária um resumo curto das decisões e o caminho do arquivo.
