# Agente Planejador MS Project

Agente de IA (via Claude API) que conversa em português, monta o cronograma
de um projeto (EAP/WBS, durações, dependências, recursos e custos) e exporta
o plano para um arquivo `.xml` que abre diretamente no Microsoft Project.

## Como funciona

Diferente de um GPT customizado (cujas instruções internas não são
acessíveis por um link público), este agente é implementado como código: um
loop de conversa com a Claude API que usa *tool use* (function calling) para
manipular o estado do projeto. As tools disponíveis para o modelo são:

- `definir_projeto` — nome, descrição, data de início.
- `adicionar_recurso` — pessoas/equipes com custo por hora.
- `adicionar_tarefa` — cria/atualiza uma tarefa. Se você informar
  **quantidade** + **índice de produtividade** (unidades por recurso por
  dia), a duração é **calculada automaticamente**
  (`duração = quantidade / (produtividade × nº de recursos alocados)`).
- `remover_tarefa`
- `calcular_cronograma` — recalcula datas (respeitando dependências
  fim-início) e custos de todas as tarefas.
- `exportar_ms_project` — gera o `.xml` compatível com o MS Project.

O estado do plano é salvo automaticamente em um JSON local a cada mudança,
então você pode fechar e continuar depois de onde parou.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edite com sua chave da Anthropic
export ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

Chave de API: crie em https://console.anthropic.com/settings/keys

## Uso

```bash
python -m agente_planejador_ms_project [arquivo_estado.json]
```

Exemplo de conversa:

```
Você: Preciso planejar a reforma de uma cozinha de 20m2. Tenho 1 pedreiro
(R$ 30/hora) e 1 eletricista (R$ 40/hora).

Agente: [pergunta produtividades faltantes / monta as tarefas com as tools]

Você: A produtividade de alvenaria é 15m2/dia por pedreiro, e a instalação
elétrica é uma tarefa de 2 dias fixos.

Agente: [chama adicionar_tarefa, calcular_cronograma e mostra o resumo]

Você: Gera o arquivo para o MS Project

Agente: [chama exportar_ms_project] Pronto, gerei plano.xml.
```

Comandos especiais (não passam pelo modelo, executam direto):

- `/plano` — mostra o resumo do cronograma atual.
- `/salvar [arquivo]` — salva o estado em JSON.
- `/exportar <arquivo.xml>` — exporta direto para MS Project XML.
- `/sair` — encerra (salva automaticamente antes de sair).

## Limitações conhecidas

- O cronograma usa uma passada simples de datas (fim-início entre
  predecessoras), sem calendário de feriados nem relações do tipo
  início-início/fim-fim.
- O XML gerado cobre os campos essenciais para importação no MS Project
  (tarefas, durações, datas, predecessoras, recursos, atribuições); recursos
  avançados do MS Project (calendários customizados, custos por tipo de
  alocação, baseline) não são exportados.

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes cobrem o cálculo de cronograma/custos e a geração do XML — não
fazem chamadas à API (não precisam de `ANTHROPIC_API_KEY`).
