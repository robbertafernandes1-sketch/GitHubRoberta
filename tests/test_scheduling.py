import pytest

from agente_planejador_ms_project.models import Project, Resource, Task
from agente_planejador_ms_project.scheduling import (
    SchedulingError,
    compute_schedule,
    compute_task_duration,
    project_duration_days,
    project_total_cost,
)


def test_duration_from_productivity_single_resource():
    task = Task(id="t1", name="Alvenaria", quantity=100, unit="m2", productivity_rate=20, resource_ids=["r1"])
    assert compute_task_duration(task) == 5.0


def test_duration_rounds_up_and_scales_with_resources():
    # 100 / (30 * 2) = 1.666... -> arredonda para cima (2 casas decimais)
    task = Task(id="t1", name="Alvenaria", quantity=100, unit="m2", productivity_rate=30, resource_ids=["r1", "r2"])
    assert compute_task_duration(task) == 1.67


def test_duration_fixed_when_no_quantity():
    task = Task(id="t1", name="Marco", duration_days=3)
    assert compute_task_duration(task) == 3


def test_milestone_zero_duration_without_quantity():
    task = Task(id="t1", name="Entrega", milestone=True)
    assert compute_task_duration(task) == 0.0


def test_missing_duration_data_raises():
    task = Task(id="t1", name="Sem dados")
    with pytest.raises(SchedulingError):
        compute_task_duration(task)


def test_zero_productivity_raises():
    task = Task(id="t1", name="X", quantity=10, productivity_rate=0)
    with pytest.raises(SchedulingError):
        compute_task_duration(task)


def _sample_project() -> Project:
    project = Project(name="Reforma", start_date="2026-01-05", skip_weekends=False)
    project.resources["pedreiro"] = Resource(id="pedreiro", name="Pedreiro", cost_per_hour=25.0)
    project.tasks["fundacao"] = Task(
        id="fundacao", name="Fundação", quantity=40, unit="m3", productivity_rate=10,
        resource_ids=["pedreiro"],
    )
    project.tasks["alvenaria"] = Task(
        id="alvenaria", name="Alvenaria", quantity=100, unit="m2", productivity_rate=20,
        resource_ids=["pedreiro"], predecessors=["fundacao"],
    )
    project.tasks["entrega"] = Task(id="entrega", name="Entrega", milestone=True, predecessors=["alvenaria"])
    return project


def test_compute_schedule_sequential_dependencies():
    project = _sample_project()
    compute_schedule(project)

    fundacao = project.tasks["fundacao"]
    alvenaria = project.tasks["alvenaria"]
    entrega = project.tasks["entrega"]

    assert fundacao.start_day == 0
    assert fundacao.computed_duration_days == 4.0
    assert fundacao.finish_day == 4

    assert alvenaria.start_day == 4
    assert alvenaria.computed_duration_days == 5.0
    assert alvenaria.finish_day == 9

    assert entrega.start_day == 9
    assert entrega.finish_day == 9

    assert project_duration_days(project) == 9


def test_compute_schedule_costs():
    project = _sample_project()
    compute_schedule(project)
    fundacao = project.tasks["fundacao"]
    # 4 dias * 8h * 25/h = 800
    assert fundacao.cost == 800.0
    assert project_total_cost(project) > 0


def test_cyclic_dependency_raises():
    project = Project()
    project.tasks["a"] = Task(id="a", name="A", duration_days=1, predecessors=["b"])
    project.tasks["b"] = Task(id="b", name="B", duration_days=1, predecessors=["a"])
    with pytest.raises(SchedulingError):
        compute_schedule(project)


def test_missing_predecessor_raises():
    project = Project()
    project.tasks["a"] = Task(id="a", name="A", duration_days=1, predecessors=["nao_existe"])
    with pytest.raises(SchedulingError):
        compute_schedule(project)
