"""CLI interativa do Agente Planejador MS Project.

Uso:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m agente_planejador_ms_project [arquivo_estado.json]

Comandos durante a conversa:
    /salvar [arquivo]     salva o estado do plano em JSON
    /exportar <arquivo.xml>  exporta o plano atual para MS Project XML
    /plano                mostra o resumo do plano atual
    /sair                 encerra
"""
from __future__ import annotations

import json
import os
import sys

from .agent import PlannerAgent
from .models import Project
from .msproject_export import export_to_msproject_xml
from .scheduling import compute_schedule, project_duration_days, project_total_cost

DEFAULT_STATE_FILE = "plano_projeto.json"


def load_project(path: str) -> Project:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return Project.from_dict(json.load(f))
    return Project()


def save_project(project: Project, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)


def print_plan_summary(project: Project) -> None:
    if not project.tasks:
        print("(nenhuma tarefa cadastrada ainda)")
        return
    try:
        compute_schedule(project)
    except Exception as e:  # noqa: BLE001
        print(f"Não foi possível calcular o cronograma: {e}")
        return
    print(f"\nProjeto: {project.name}")
    print(f"{'ID':<8}{'Tarefa':<30}{'Dur.(d)':<10}{'Início':<8}{'Fim':<8}{'Custo':<12}")
    for t in sorted(project.tasks.values(), key=lambda x: x.start_day or 0):
        print(
            f"{t.id:<8}{t.name[:28]:<30}{t.computed_duration_days:<10}"
            f"{t.start_day:<8}{t.finish_day:<8}{t.cost or 0:<12.2f}"
        )
    print(f"\nDuração total: {project_duration_days(project)} dias")
    print(f"Custo total: {project_total_cost(project):.2f}\n")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ERRO: defina a variável de ambiente ANTHROPIC_API_KEY antes de rodar.\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...",
            file=sys.stderr,
        )
        sys.exit(1)

    state_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STATE_FILE
    project = load_project(state_file)

    def autosave():
        save_project(project, state_file)

    agent = PlannerAgent(project=project, on_change=autosave)

    print("Agente Planejador MS Project. Digite /sair para encerrar, /plano para ver o resumo.")
    if project.tasks:
        print(f"(estado carregado de {state_file}: {len(project.tasks)} tarefa(s))")

    while True:
        try:
            user_input = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input in ("/sair", "/exit", "/quit"):
            break
        if user_input == "/plano":
            print_plan_summary(project)
            continue
        if user_input.startswith("/salvar"):
            parts = user_input.split(maxsplit=1)
            path = parts[1] if len(parts) > 1 else state_file
            save_project(project, path)
            print(f"Estado salvo em {path}")
            continue
        if user_input.startswith("/exportar"):
            parts = user_input.split(maxsplit=1)
            if len(parts) < 2:
                print("Uso: /exportar caminho.xml")
                continue
            try:
                path = export_to_msproject_xml(project, parts[1])
                print(f"Exportado para {path}")
            except Exception as e:  # noqa: BLE001
                print(f"Erro ao exportar: {e}")
            continue

        try:
            reply = agent.send(user_input)
        except Exception as e:  # noqa: BLE001
            print(f"Erro ao chamar o modelo: {e}")
            continue
        print(f"\nAgente: {reply}")

    save_project(project, state_file)
    print(f"Estado salvo em {state_file}. Até mais!")


if __name__ == "__main__":
    main()
