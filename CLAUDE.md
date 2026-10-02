# Assistente de Planejamento — Montagem Industrial

## O que é
Assistente de planejamento para obras de montagem industrial. Ele lê o cronograma e a medição de campo em CSV, aponta erros e riscos, propõe correções e, com aprovação, grava um cronograma corrigido. Também mede os desvios e audita o cronograma pelos 14 pontos do DCMA.

## Stack
- Python 3, com scripts versionados neste repositório.
- Entrada em CSV (cronograma, medição, feriados) e configuração por obra.
- Saída: relatórios em planilha Excel (.xlsx).

## Regras que nunca podem ser quebradas
1. Nunca alterar o CSV original do cronograma nem o da medição. Correções vão sempre para um arquivo novo `*_corrigido.csv`.
2. Nenhuma correção é gravada sem aprovação explícita da usuária, uma a uma.
3. Todo cálculo (caminho crítico, folgas, DCMA, desvios) sai do script, nunca de conta feita de cabeça.
4. Ponto do DCMA sem dado de entrada é "N/A – dado ausente", nunca aprovado.
5. Durações em dias úteis no calendário da obra (seg-sáb + feriados), nunca em dias corridos.
6. Não perguntar o que dá para descobrir lendo os arquivos.

## Documentos de referência
- Decisões de projeto: `docs/fase-1-grill-me.md`. Consulte-o antes de mudar formato, calendário, limites ou fluxo.
- Vocabulário de planejamento (EAP, TI/II/TT, folga, caminho crítico...): `CONTEXT.md`.
- Arquivos de cada obra: `docs/obras/<nome-da-obra>/`.
- Skills do projeto: `.claude/skills/` (`/grill-me` para entrevistar sobre um plano, `/revisar-cronograma` para revisar antes do cliente, `/auditoria-dcma` para o placar dos 14 pontos).
