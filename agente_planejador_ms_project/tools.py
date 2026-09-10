"""Definição das tools (function calling) expostas ao modelo e o dispatcher
que as executa sobre um Project em memória."""
from __future__ import annotations

from typing import Any, Callable

from .models import Project, Resource, Task
from .scheduling import SchedulingError, compute_schedule, project_duration_days, project_total_cost
from .msproject_export import export_to_msproject_xml

TOOLS: list[dict[str, Any]] = [
    {
        "name": "definir_projeto",
        "description": "Define ou atualiza as informações gerais do projeto (nome, descrição, data de início).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "start_date": {
                    "type": "string",
                    "description": "Data de início no formato AAAA-MM-DD",
                },
                "skip_weekends": {
                    "type": "boolean",
                    "description": "Se true, cronograma considera apenas dias úteis (padrão true)",
                },
            },
            "required": ["name"],
        },
    },
    {
        "name": "adicionar_recurso",
        "description": "Adiciona ou atualiza um recurso (pessoa/equipe/equipamento) disponível para alocação.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Identificador curto único, ex: 'pedreiro1'"},
                "name": {"type": "string"},
                "role": {"type": "string"},
                "cost_per_hour": {"type": "number", "description": "Custo por hora"},
                "hours_per_day": {"type": "number", "description": "Jornada diária em horas (padrão 8)"},
            },
            "required": ["id", "name"],
        },
    },
    {
        "name": "adicionar_tarefa",
        "description": (
            "Adiciona ou atualiza uma tarefa do cronograma. A duração é calculada "
            "automaticamente a partir de quantidade/produtividade quando ambos são "
            "informados; caso contrário use duration_days para duração fixa (ex: marcos)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Identificador curto único, ex: 't1'"},
                "name": {"type": "string"},
                "quantity": {"type": "number", "description": "Quantidade de serviço, ex: 120 (m²)"},
                "unit": {"type": "string", "description": "Unidade, ex: 'm²', 'm³', 'un'"},
                "productivity_rate": {
                    "type": "number",
                    "description": "Índice de produtividade: unidades por recurso por dia",
                },
                "duration_days": {
                    "type": "number",
                    "description": "Duração fixa em dias, usada quando não há quantidade/produtividade",
                },
                "predecessors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs das tarefas predecessoras (fim-início)",
                },
                "resource_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs dos recursos alocados a esta tarefa",
                },
                "milestone": {"type": "boolean"},
            },
            "required": ["id", "name"],
        },
    },
    {
        "name": "remover_tarefa",
        "description": "Remove uma tarefa do cronograma pelo id.",
        "input_schema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
    },
    {
        "name": "calcular_cronograma",
        "description": (
            "Recalcula datas, durações e custos de todas as tarefas com base nas "
            "dependências, produtividade e recursos alocados. Retorna o resumo do plano."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "exportar_ms_project",
        "description": "Exporta o plano atual para um arquivo .xml compatível com o Microsoft Project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Caminho do arquivo .xml de saída"},
            },
            "required": ["filepath"],
        },
    },
]


def _task_summary(task: Task) -> dict:
    return {
        "id": task.id,
        "name": task.name,
        "duration_days": task.computed_duration_days,
        "start_day": task.start_day,
        "finish_day": task.finish_day,
        "predecessors": task.predecessors,
        "resource_ids": task.resource_ids,
        "cost": task.cost,
    }


def make_dispatcher(project: Project, on_change: Callable[[], None] | None = None):
    """Retorna uma função dispatch(tool_name, tool_input) -> dict/str que
    executa a tool sobre o `project` fornecido."""

    def dispatch(name: str, tool_input: dict) -> Any:
        try:
            if name == "definir_projeto":
                project.name = tool_input["name"]
                project.description = tool_input.get("description", project.description)
                if "start_date" in tool_input:
                    project.start_date = tool_input["start_date"]
                if "skip_weekends" in tool_input:
                    project.skip_weekends = tool_input["skip_weekends"]
                result = {"ok": True, "project": project.name}

            elif name == "adicionar_recurso":
                project.resources[tool_input["id"]] = Resource(
                    id=tool_input["id"],
                    name=tool_input["name"],
                    role=tool_input.get("role", ""),
                    cost_per_hour=tool_input.get("cost_per_hour", 0.0),
                    hours_per_day=tool_input.get("hours_per_day", 8.0),
                )
                result = {"ok": True, "resource_id": tool_input["id"]}

            elif name == "adicionar_tarefa":
                project.tasks[tool_input["id"]] = Task(
                    id=tool_input["id"],
                    name=tool_input["name"],
                    quantity=tool_input.get("quantity"),
                    unit=tool_input.get("unit", ""),
                    productivity_rate=tool_input.get("productivity_rate"),
                    duration_days=tool_input.get("duration_days"),
                    predecessors=tool_input.get("predecessors", []),
                    resource_ids=tool_input.get("resource_ids", []),
                    milestone=tool_input.get("milestone", False),
                )
                result = {"ok": True, "task_id": tool_input["id"]}

            elif name == "remover_tarefa":
                project.tasks.pop(tool_input["id"], None)
                result = {"ok": True}

            elif name == "calcular_cronograma":
                compute_schedule(project)
                result = {
                    "tasks": [_task_summary(t) for t in project.tasks.values()],
                    "total_duration_days": project_duration_days(project),
                    "total_cost": project_total_cost(project),
                }

            elif name == "exportar_ms_project":
                path = export_to_msproject_xml(project, tool_input["filepath"])
                result = {"ok": True, "filepath": path}

            else:
                result = {"error": f"Tool desconhecida: {name}"}

        except SchedulingError as e:
            result = {"error": str(e)}
        except Exception as e:  # noqa: BLE001 - devolve o erro ao modelo, não trava o loop
            result = {"error": f"{type(e).__name__}: {e}"}

        if on_change is not None:
            on_change()
        return result

    return dispatch
