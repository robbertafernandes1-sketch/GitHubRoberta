"""Modelos de dados do plano de projeto: tarefas, recursos e o projeto em si."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Resource:
    id: str
    name: str
    role: str = ""
    cost_per_hour: float = 0.0
    hours_per_day: float = 8.0

    @property
    def cost_per_day(self) -> float:
        return self.cost_per_hour * self.hours_per_day


@dataclass
class Task:
    id: str
    name: str
    quantity: Optional[float] = None
    unit: str = ""
    productivity_rate: Optional[float] = None  # unidades por recurso por dia
    duration_days: Optional[float] = None  # usado quando não há quantidade/produtividade
    predecessors: list[str] = field(default_factory=list)
    resource_ids: list[str] = field(default_factory=list)
    milestone: bool = False

    # Preenchidos pelo cálculo de cronograma
    computed_duration_days: Optional[float] = None
    start_day: Optional[int] = None
    finish_day: Optional[int] = None
    cost: Optional[float] = None


@dataclass
class Project:
    name: str = "Novo Projeto"
    description: str = ""
    start_date: str = ""  # ISO "YYYY-MM-DD"
    skip_weekends: bool = True
    tasks: dict[str, Task] = field(default_factory=dict)
    resources: dict[str, Resource] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "skip_weekends": self.skip_weekends,
            "tasks": {k: asdict(v) for k, v in self.tasks.items()},
            "resources": {k: asdict(v) for k, v in self.resources.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        proj = cls(
            name=data.get("name", "Novo Projeto"),
            description=data.get("description", ""),
            start_date=data.get("start_date", ""),
            skip_weekends=data.get("skip_weekends", True),
        )
        for tid, t in data.get("tasks", {}).items():
            proj.tasks[tid] = Task(**t)
        for rid, r in data.get("resources", {}).items():
            proj.resources[rid] = Resource(**r)
        return proj
