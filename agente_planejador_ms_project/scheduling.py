"""Cálculo de durações (por índice de produtividade), datas (CPM simples) e custos."""
from __future__ import annotations

import math
from datetime import date, timedelta

from .models import Project, Task


class SchedulingError(Exception):
    pass


def compute_task_duration(task: Task) -> float:
    """Duração em dias.

    Se a tarefa tiver quantidade + índice de produtividade, a duração é
    calculada como quantidade / (produtividade * nº de recursos alocados),
    arredondada para cima. Caso contrário usa a duração informada manualmente.
    """
    if task.quantity is not None and task.productivity_rate:
        if task.productivity_rate <= 0:
            raise SchedulingError(
                f"Tarefa '{task.id}': índice de produtividade deve ser positivo"
            )
        num_resources = max(1, len(task.resource_ids))
        duration = task.quantity / (task.productivity_rate * num_resources)
        return math.ceil(duration * 100) / 100  # arredonda para cima, 2 casas
    if task.duration_days is not None:
        return task.duration_days
    if task.milestone:
        return 0.0
    raise SchedulingError(
        f"Tarefa '{task.id}': informe quantidade+produtividade ou duration_days"
    )


def _topological_order(tasks: dict[str, Task]) -> list[str]:
    visited: dict[str, int] = {}  # 0 = em andamento, 1 = concluído
    order: list[str] = []

    def visit(tid: str, stack: list[str]):
        if tid not in tasks:
            raise SchedulingError(
                f"Predecessora '{tid}' referenciada não existe (em {stack[-1] if stack else '?'})"
            )
        state = visited.get(tid)
        if state == 1:
            return
        if state == 0:
            raise SchedulingError(f"Dependência cíclica detectada envolvendo '{tid}'")
        visited[tid] = 0
        for pred in tasks[tid].predecessors:
            visit(pred, stack + [tid])
        visited[tid] = 1
        order.append(tid)

    for tid in tasks:
        visit(tid, [])
    return order


def _add_business_days(start: date, days: float, skip_weekends: bool) -> date:
    """Soma 'days' dias corridos ou úteis a partir de start."""
    if not skip_weekends:
        return start + timedelta(days=days)
    whole = int(days)
    frac = days - whole
    d = start
    added = 0
    while added < whole:
        d += timedelta(days=1)
        if d.weekday() < 5:
            added += 1
    if frac > 0:
        d += timedelta(days=1 if d.weekday() < 4 else 3)
    return d


def compute_schedule(project: Project) -> None:
    """Preenche computed_duration_days, start_day/finish_day (índice em dias
    corridos desde o início do projeto) e cost em cada tarefa, in-place."""
    order = _topological_order(project.tasks)

    finish_offset: dict[str, float] = {}
    for tid in order:
        task = project.tasks[tid]
        duration = compute_task_duration(task)
        task.computed_duration_days = duration

        if task.predecessors:
            start_offset = max(finish_offset[p] for p in task.predecessors)
        else:
            start_offset = 0.0

        task.start_day = round(start_offset)
        finish = start_offset + duration
        task.finish_day = round(finish)
        finish_offset[tid] = finish

        cost = 0.0
        for rid in task.resource_ids:
            resource = project.resources.get(rid)
            if resource is not None:
                cost += resource.cost_per_day * duration
        task.cost = round(cost, 2)


def project_duration_days(project: Project) -> float:
    if not project.tasks:
        return 0.0
    return max((t.finish_day or 0) for t in project.tasks.values())


def project_total_cost(project: Project) -> float:
    return round(sum((t.cost or 0.0) for t in project.tasks.values()), 2)


def task_calendar_dates(project: Project, task: Task) -> tuple[date, date]:
    """Converte start_day/finish_day (offsets) em datas reais a partir de
    project.start_date, respeitando skip_weekends."""
    if not project.start_date:
        base = date.today()
    else:
        base = date.fromisoformat(project.start_date)
    start = _add_business_days(base, task.start_day or 0, project.skip_weekends)
    finish = _add_business_days(base, task.finish_day or 0, project.skip_weekends)
    return start, finish
