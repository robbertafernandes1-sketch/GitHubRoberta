---
name: auditoria-dcma
description: Audita um cronograma de obra de montagem industrial pelos 14 pontos do DCMA (lógica, leads, lags, tipos de relação, restrições, folga alta, folga negativa, duração alta, datas inválidas, recursos, tarefas perdidas, teste do caminho crítico, CPLI e BEI) e devolve o placar. Use quando a usuária pedir "auditoria DCMA", "roda os 14 pontos", "o cronograma passa no DCMA?" ou invocar /auditoria-dcma.
---

# Auditoria DCMA

Audite o cronograma pelos 14 pontos do DCMA e devolva o placar. A auditoria só lê os arquivos: não altera nada e não propõe correções. Para corrigir, use `/revisar-cronograma`.

## 1. Reunir os arquivos

- **Cronograma:** use o CSV indicado ou a tabela colada. Uma tabela colada vira um CSV no scratchpad da sessão. Se não houver indicação, procure em `docs/obras/*/`. Se houver mais de um candidato, pergunte qual com `AskUserQuestion`.
- **Na pasta da obra, se existirem:**
  - a configuração (data de início, data contratual, limites próprios);
  - o `feriados.csv`;
  - a medição mais recente, com a data de corte;
  - a linha de base (o `*_corrigido.csv` aprovado).
- **Não peça** o que não existe para "completar" a auditoria. Ponto sem dado é não avaliável.

## 2. Carregar os pontos

Só agora leia `dcma-14-pontos.md`, nesta mesma pasta. É lá que estão o universo de contagem, a forma de medir, o limite e o dado exigido de cada ponto. Se a configuração da obra tiver limites próprios, eles substituem os padrões, e o placar indica qual limite foi usado.

## 3. Medir por script

- Todo número sai de código, nunca de conta de cabeça. Se o repositório já tiver o script de análise, use-o. Senão, escreva um script Python descartável no scratchpad e rode-o.
- Rode no calendário da obra: dias úteis de segunda a sábado, menos os feriados.
- **Marcos (duração 0) ficam fora de todas as contagens.**
- Se a rede tiver erro estrutural (ciclo, predecessora inexistente, duração inválida), os pontos que dependem do cálculo de caminho crítico ficam **não avaliáveis**, com o motivo.

## 4. Devolver o placar

Responda na conversa:

1. **Resumo:** "X passam · Y falham · Z não avaliáveis (de 14)", mais a data de corte e o tamanho do universo de contagem (quantas atividades e quantos vínculos).
2. **Placar** em tabela: # | Ponto | Medida (numerador/denominador) | Resultado | Limite | Situação.
   - A situação é **passa**, **falha** ou **não avaliável — <motivo>** (ex.: "sem coluna `recurso`", "sem medição", "sem linha de base").
   - Nunca marque **passa** sem ter medido. Na dúvida, o ponto é não avaliável.
3. **Detalhe das falhas:** para cada ponto que falhou, os IDs e as descrições das atividades ou dos vínculos que causaram a falha. Se forem mais de 10, mostre os 10 primeiros e o total.

Não dê veredito sobre apresentar o cronograma ao cliente. Esse papel é da `/revisar-cronograma`.
