---
name: revisar-cronograma
description: Revisa um cronograma de obra de montagem industrial (tabela colada na conversa ou CSV em docs/obras/) e aponta erros e riscos antes de apresentá-lo ao cliente. Use quando a usuária pedir "revisa o cronograma", "confere antes de mandar pro cliente", "tem algum problema nesse cronograma?" ou invocar /revisar-cronograma.
---

# Revisar Cronograma

Revise o cronograma e entregue uma lista de problemas pronta para a usuária corrigir antes de apresentar ao cliente. Fale como planejador, usando os termos de `CONTEXT.md`.

## 1. Obter o cronograma

- **CSV:** use o caminho informado. Se não houver caminho, procure em `docs/obras/*/`. Se houver mais de um candidato, pergunte qual com `AskUserQuestion`.
- **Tabela colada:** salve-a como CSV no scratchpad da sessão, nunca em `docs/`, e trabalhe sobre essa cópia.
- **Nunca altere o arquivo original.**
- Confira se existem as colunas esperadas: ID, descrição, duração em dias úteis e predecessoras no formato `10FS;20SS+2`. Também podem vir as colunas opcionais `restricao`, `data_restricao`, `recurso` e `disciplina`. Se faltar uma coluna obrigatória ou o formato for ambíguo, pergunte antes de seguir. Não adivinhe.
- Leia também, se existirem na pasta da obra, a configuração (data de início e limites), o `feriados.csv` e a medição mais recente.

## 2. Carregar as regras

Só agora leia `regras-de-risco.md`, nesta mesma pasta. É lá que estão as checagens, os limites padrão e a severidade de cada problema. Se a configuração da obra tiver limites próprios, eles substituem os padrões.

## 3. Calcular por script

Todo número (contagens, percentuais, caminho crítico, folgas, datas) sai de código, nunca de conta de cabeça. Esta é a regra 3 do `CLAUDE.md`.

- Se o repositório já tiver o script de análise, rode-o.
- Se ainda não tiver, escreva um script Python descartável no scratchpad, que faça só o que as regras pedem, e rode-o. Não deixe esse script em `docs/` nem na raiz.
- Rode no calendário da obra: segunda a sábado, menos os feriados.

## 4. Apresentar o resultado

Responda na conversa, nesta ordem:

1. **Veredito em uma linha:** "Pode ir ao cliente", "Pode ir com ressalvas" ou "Não apresentar ainda".
2. **Bloqueadores:** problemas de severidade alta. Para cada um, informe a atividade (ID e descrição), o problema, o dado que o comprova e a correção proposta.
3. **Atenção:** problemas de severidade média, no mesmo formato.
4. **Placar DCMA:** os 14 pontos, cada um com resultado, limite e situação (aprovado, reprovado ou "N/A – dado ausente").
5. **Caminho crítico:** a sequência de IDs, a duração total e a data de término prevista.

Seja direta. Não liste o que está correto, além do placar.

## 5. Correções

- Só proponha correções. Não grave nada sem aprovação.
- Se a usuária quiser aplicar as correções, pergunte uma a uma com `AskUserQuestion`. As opções são aprovar (recomendado, quando for o caso), rejeitar e ajustar.
- Grave só as aprovadas em `<nome>_corrigido.csv`, ao lado do original, com um log das alterações.
- Se a tabela tiver sido colada, gere o corrigido no scratchpad e entregue-o à usuária.
