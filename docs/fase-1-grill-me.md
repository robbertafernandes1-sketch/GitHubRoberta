# Fase 1 — Grill Me

**Data:** 2026-10-01
**Plano:** Assistente de planejamento para obras de montagem industrial. Ele lê o cronograma (CSV com atividades, durações em dias úteis e predecessoras) e a medição de campo, aponta erros e riscos, propõe correções e, com aprovação, grava um CSV corrigido sem alterar o original. Também mede os desvios e audita o cronograma pelos 14 pontos do DCMA.

## Decisões

| # | Pergunta | Decisão | Recomendação do Claude |
|---|----------|---------|------------------------|
| 1 | Como fazer os cálculos (CPM, folgas, DCMA, desvios)? | Tudo por script, inclusive apontar riscos e propor correções por regras fixas | Híbrido: julgamento do Claude + contas por script (não seguida) |
| 2 | Formato das predecessoras no CSV | ID com tipo e lag, ex.: `10FS;20SS+2;30FF-1` (FS/SS/FF/SF, lag e lead) | Tipo e lag (seguida) |
| 3 | Calendário | Segunda a sábado + feriados nacionais + `feriados.csv` opcional por obra; data de início em arquivo de configuração | Seg-sáb + feriados (seguida) |
| 4 | Conteúdo da medição de campo | Por atividade: início real, término real (se terminou) e % físico na data de corte | Datas reais + % (seguida) |
| 5 | Pontos do DCMA sem dado (5 restrições, 10 recursos, 14 BEI) | Colunas opcionais `restricao`, `data_restricao`, `recurso`; se faltar a coluna, o ponto sai como "N/A – dado ausente", nunca como aprovado | Colunas opcionais (seguida) |
| 6 | Limites do DCMA | Limites oficiais (ex.: 44 dias úteis para folga e duração altas, 5% para leads, lags e restrições) num arquivo de configuração, ajustáveis por obra | Padrão, configurável (seguida) |
| 7 | Aprovação das correções | Uma a uma, com opções para clicar (aprovar, rejeitar, ajustar); só as aprovadas entram em `<nome>_corrigido.csv`, com log de alterações | Uma a uma (seguida) |
| 8 | Formato dos relatórios | Planilha Excel (.xlsx), uma aba por análise, com formatação condicional | Markdown + CSV (não seguida) |
| 9 | Organização das obras | Uma pasta por obra: `docs/obras/<nome-da-obra>/` (cronograma, medições por data de corte, configuração, relatórios) | Uma pasta por obra (seguida) |
| 10 | Linha de base para desvios e BEI | O CSV corrigido e aprovado, congelado; o original fica como referência histórica | O corrigido aprovado (seguida) |

## Fatos encontrados nos arquivos

- O repositório ainda não tinha `docs/` nem nenhum cronograma ou medição. Por isso o formato do CSV foi decidido nesta entrevista, e não lido de um arquivo.
- Em `.claude/skills/` só existem as skills `find-skills`, `frontend-design` e `grill-me`. Ainda não há código.

## Pontos em aberto

- **Regras de sequência de montagem** (ex.: teste hidrostático antes de isolamento e pintura, comissionamento depois da montagem elétrica). A pergunta foi interrompida e ficou sem resposta: falta decidir se entram, e se as atividades seriam identificadas por palavra-chave no nome ou por uma coluna de disciplina.
- **Nomes exatos das colunas** do CSV de cronograma e do CSV de medição.
- **Volume da aprovação uma a uma**: em cronogramas grandes, a lista de correções pode ficar longa. Talvez valha agrupar as correções idênticas.
- **Biblioteca para o Excel**: a stack proposta é Python + openpyxl, mas ainda não foi confirmada.

## Próximos passos

- Definir o layout dos CSVs (cronograma, medição, feriados) e do arquivo de configuração por obra.
- Implementar o script: leitura e validação, CPM com calendário seg-sáb, as checagens DCMA, a proposta de correções, a gravação do corrigido com log, os desvios e o relatório .xlsx.
- Testar com o primeiro cronograma real colocado em `docs/obras/<obra>/`.
