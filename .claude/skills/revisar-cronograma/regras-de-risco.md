# Regras de Risco — Revisão de Cronograma

Arquivo lido pela skill `revisar-cronograma` no passo 2. Os limites abaixo são o padrão; a configuração de cada obra pode substituí-los (ver `docs/fase-1-grill-me.md`, decisão 6). Severidade: **alta** = bloqueador, **média** = atenção.

## A. Erros estruturais (antes de qualquer cálculo)

| # | Regra | Severidade |
|---|-------|------------|
| A1 | ID duplicado ou vazio | alta |
| A2 | Predecessora que aponta para ID inexistente | alta |
| A3 | Ciclo lógico (A depende de B que depende de A) | alta |
| A4 | Duração ausente, negativa ou não numérica | alta |
| A5 | Predecessora fora do formato `<ID><FS\|SS\|FF\|SF>[+/-n]` | alta |
| A6 | Mais de uma atividade sem predecessora (início em aberto) ou sem sucessora (fim em aberto); o esperado é um único marco de início e um único de fim | alta |
| A7 | Atividade dependente de si mesma ou vínculo duplicado entre o mesmo par | média |
| A8 | Marco (duração 0) com vínculo II/TT ou com defasagem | média |

Se A1–A5 ocorrerem, pare depois de reportá-los: o cálculo do caminho crítico não é confiável.

## B. 14 pontos do DCMA

Percentuais sobre as atividades incompletas, excluindo marcos quando o ponto for de duração. Durações e folgas em dias úteis do calendário da obra.

| # | Ponto | Critério de aprovação | Severidade se reprovar |
|---|-------|----------------------|------------------------|
| 1 | Lógica | Sem predecessora ou sem sucessora ≤ 5% | alta |
| 2 | Leads (defasagem negativa) | 0 vínculos | alta |
| 3 | Lags (defasagem positiva) | ≤ 5% dos vínculos | média |
| 4 | Tipos de vínculo | TI (FS) ≥ 90% dos vínculos | média |
| 5 | Restrições rígidas | ≤ 5% (requer coluna `restricao`) | média |
| 6 | Folga alta | Folga total > 44 dias úteis em ≤ 5% | média |
| 7 | Folga negativa | 0 atividades | alta |
| 8 | Duração alta | Duração > 44 dias úteis em ≤ 5% | média |
| 9 | Datas inválidas | 0 datas reais após a data de corte ou previsões antes dela (requer medição) | alta |
| 10 | Recursos | Toda atividade com duração > 0 tem recurso (requer coluna `recurso`) | média |
| 11 | Tarefas perdidas | ≤ 5% das que deviam ter terminado na linha de base terminaram depois (requer medição e linha de base) | média |
| 12 | Teste do caminho crítico | Atrasar uma atividade crítica atrasa o término na mesma medida | alta |
| 13 | CPLI | ≥ 0,95 (requer medição) | alta |
| 14 | BEI | ≥ 0,95 (requer medição e linha de base = cronograma corrigido aprovado) | média |

Dado de entrada ausente → "N/A – dado ausente". Nunca marcar como aprovado.

## C. Riscos de prazo para o cliente

| # | Regra | Severidade |
|---|-------|------------|
| C1 | Término calculado posterior à data contratual (se informada na configuração) | alta |
| C2 | Caminho crítico com mais de 50% das atividades da obra — prazo sem gordura | média |
| C3 | Caminho crítico concentrado numa única disciplina ou frente (requer coluna `disciplina`) | média |
| C4 | Atividade crítica atravessando feriado ou parada da planta do `feriados.csv` | média |
| C5 | Medição: atividade crítica com % físico abaixo do previsto na data de corte | alta |

## D. Sequência construtiva de montagem — em avaliação

Ponto em aberto em `docs/fase-1-grill-me.md` (falta decidir se entra e se usa nome ou coluna `disciplina`). Até decidir, reportar só como **atenção**, identificando pelo nome da atividade, e avisar que a regra está em avaliação.

| # | Sucessora | Deve ter antes (direta ou indiretamente) |
|---|-----------|------------------------------------------|
| D1 | Montagem de estrutura / equipamento | Base civil / fundação |
| D2 | Isolamento térmico, pintura final | Teste hidrostático / pneumático |
| D3 | Comissionamento | Montagem elétrica e instrumentação |
| D4 | Teste hidrostático | Montagem de tubulação do mesmo sistema |
