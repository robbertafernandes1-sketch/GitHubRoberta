"""Loop de conversa com a Claude API usando tool use (function calling)."""
from __future__ import annotations

import json
import os

from .models import Project
from .tools import TOOLS, make_dispatcher

DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

SYSTEM_PROMPT = """\
Você é o Agente Planejador MS Project, especialista em planejamento e controle
de projetos (cronogramas, EAP/WBS, alocação de recursos e custos), falando
sempre em português do Brasil.

Seu trabalho, a partir da descrição do projeto que o usuário fornecer:
1. Estruturar as entregas em uma EAP/WBS com tarefas claras.
2. Para cada tarefa de serviço mensurável, obter do usuário (ou estimar de
   forma explícita, avisando que é uma estimativa) a quantidade, a unidade e
   o índice de produtividade (unidades por recurso por dia). A duração é
   sempre calculada a partir desses dados via a tool `adicionar_tarefa`
   (nunca invente a duração diretamente quando houver quantidade e
   produtividade disponíveis).
3. Definir dependências entre tarefas (predecessoras) de forma realista.
4. Alocar recursos (pessoas/equipes) às tarefas usando `adicionar_recurso` e
   o campo resource_ids de `adicionar_tarefa`.
5. Sempre que o plano mudar, chamar `calcular_cronograma` para recalcular
   datas e custos, e apresentar um resumo claro (tabela em texto) ao usuário:
   tarefa, duração, início/fim (em dias a partir do início do projeto), custo.
6. Quando o usuário pedir para gerar o arquivo do MS Project, usar a tool
   `exportar_ms_project` com um caminho de arquivo .xml.

Use as tools disponíveis para qualquer alteração de estado do plano — não
apenas descreva em texto o que faria. Depois de usar as tools, sempre
resuma o resultado em linguagem natural para o usuário. Seja direto e
objetivo. Se faltar informação essencial (ex: produtividade de um serviço),
pergunte ao usuário antes de assumir um valor.
"""


class PlannerAgent:
    def __init__(
        self,
        project: Project | None = None,
        model: str = DEFAULT_MODEL,
        on_change=None,
        api_key: str | None = None,
    ):
        try:
            import anthropic
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "Pacote 'anthropic' não instalado. Rode: pip install -r requirements.txt"
            ) from e

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.project = project if project is not None else Project()
        self.dispatch = make_dispatcher(self.project, on_change=on_change)
        self.messages: list[dict] = []

    def send(self, user_message: str, max_tool_rounds: int = 12) -> str:
        self.messages.append({"role": "user", "content": user_message})

        final_text_parts: list[str] = []
        for _ in range(max_tool_rounds):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=self.messages,
            )

            assistant_content = [block.model_dump() for block in response.content]
            self.messages.append({"role": "assistant", "content": assistant_content})

            text_blocks = [b["text"] for b in assistant_content if b["type"] == "text"]
            final_text_parts.extend(text_blocks)

            if response.stop_reason != "tool_use":
                break

            tool_results = []
            for block in assistant_content:
                if block["type"] != "tool_use":
                    continue
                result = self.dispatch(block["name"], block["input"])
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
            self.messages.append({"role": "user", "content": tool_results})
        else:
            final_text_parts.append(
                "\n[Aviso: limite de chamadas de ferramentas atingido nesta rodada.]"
            )

        return "\n".join(p for p in final_text_parts if p)
