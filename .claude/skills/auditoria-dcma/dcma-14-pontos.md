# DCMA — 14 Pontos

Arquivo lido pela skill `auditoria-dcma` no passo 2. Limites padrão do DCMA; a configuração da obra pode substituí-los (`docs/fase-1-grill-me.md`, decisão 6).

## Regras gerais

- **Universo de contagem:** atividades **incompletas** (sem término real na medição; sem medição, todas), **excluindo marcos** (duração 0). Vínculos contam quando a sucessora está nesse universo.
- **Unidade:** dias úteis do calendário da obra (seg-sáb menos feriados).
- **Situações possíveis:** passa · falha · não avaliável. Faltou o dado exigido, ou a rede tem erro estrutural que impede o cálculo → **não avaliável**, com o motivo. Nunca "passa" por omissão.
- **Universo vazio** (ex.: nenhuma atividade incompleta) → não avaliável — "universo vazio".

## Os 14 pontos

| # | Ponto | Como medir | Limite (passa se) | Dado exigido |
|---|-------|-----------|-------------------|--------------|
| 1 | Lógica | Atividades sem predecessora **ou** sem sucessora ÷ universo | ≤ 5% | Cronograma |
| 2 | Leads | Vínculos com defasagem negativa (ex.: `FS-2`) | = 0 | Cronograma |
| 3 | Lags | Vínculos com defasagem positiva ÷ total de vínculos | ≤ 5% | Cronograma |
| 4 | Tipos de relação | Vínculos TI (FS) ÷ total de vínculos | ≥ 90% | Cronograma |
| 5 | Restrições rígidas | Atividades com restrição rígida ÷ universo. Rígidas: deve iniciar em, deve terminar em, iniciar no máximo em, terminar no máximo em (MSO, MFO, SNLT, FNLT) | ≤ 5% | Coluna `restricao` |
| 6 | Folga alta | Atividades com folga total > 44 dias úteis ÷ universo | ≤ 5% | Cronograma válido (CPM) |
| 7 | Folga negativa | Atividades com folga total < 0, calculada contra a data contratual ou a restrição, se houver | = 0 | Cronograma válido (CPM) |
| 8 | Duração alta | Atividades com duração (restante, se houver medição) > 44 dias úteis ÷ universo | ≤ 5% | Cronograma |
| 9 | Datas inválidas | Atividades com data real **depois** da data de corte, ou com data prevista (não iniciada/não concluída) **antes** da data de corte | = 0 | Medição com data de corte |
| 10 | Recursos | Atividades do universo sem recurso atribuído | = 0 | Coluna `recurso` |
| 11 | Tarefas perdidas | Entre as atividades com término de linha de base ≤ data de corte: as que terminaram depois da linha de base ou não terminaram ÷ esse total | ≤ 5% | Medição + linha de base |
| 12 | Teste do caminho crítico | Somar um atraso grande (ex.: 600 dias úteis) a uma atividade crítica incompleta e recalcular: o término da obra deve atrasar exatamente o mesmo valor | Atraso igual (sim/não) | Cronograma válido (CPM) |
| 13 | CPLI | (Comprimento restante do caminho crítico + folga total do término em relação à data contratual) ÷ comprimento restante do caminho crítico | ≥ 0,95 | Medição com data de corte + data contratual (ou término da linha de base) |
| 14 | BEI | Atividades concluídas ÷ atividades com término de linha de base ≤ data de corte | ≥ 0,95 | Medição + linha de base (o `*_corrigido.csv` aprovado) |

## Observações

- **Pontos 6, 7, 12 e 13** dependem do caminho crítico. Com ciclo, predecessora inexistente ou duração inválida → não avaliável — "rede com erro estrutural".
- **Ponto 7** sem data contratual nem restrições: a folga negativa é impossível por construção. Reportar "passa" com a nota "sem data contratual nem restrições — folga negativa só aparece com elas".
- **Pontos 2, 3 e 4:** se o CSV trouxer só IDs nas predecessoras (sem tipo), assumir TI sem defasagem e anotar isso no placar.
