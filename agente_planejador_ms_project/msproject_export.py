"""Exporta um Project para o formato MS Project XML (importável diretamente
no Microsoft Project: Arquivo > Abrir > selecionar o .xml)."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date, datetime
from xml.dom import minidom

from .models import Project
from .scheduling import compute_schedule, task_calendar_dates

MS_PROJECT_NS = "http://schemas.microsoft.com/project"


def _duration_iso(days: float, hours_per_day: float = 8.0) -> str:
    """Converte dias em duração ISO 8601 no formato usado pelo MS Project,
    ex.: 2 dias -> 'PT16H0M0S'."""
    total_hours = days * hours_per_day
    hours = int(total_hours)
    minutes = round((total_hours - hours) * 60)
    return f"PT{hours}H{minutes}M0S"


def _dt(d: date) -> str:
    return datetime(d.year, d.month, d.day, 8, 0, 0).isoformat()


def build_msproject_xml(project: Project) -> str:
    compute_schedule(project)

    root = ET.Element("Project", xmlns=MS_PROJECT_NS)
    ET.SubElement(root, "Name").text = project.name
    ET.SubElement(root, "Title").text = project.name
    ET.SubElement(root, "Author").text = "Agente Planejador MS Project"

    start_date = date.fromisoformat(project.start_date) if project.start_date else date.today()
    ET.SubElement(root, "StartDate").text = _dt(start_date)

    calendar_uid = "1"
    calendars = ET.SubElement(root, "Calendars")
    cal = ET.SubElement(calendars, "Calendar")
    ET.SubElement(cal, "UID").text = calendar_uid
    ET.SubElement(cal, "Name").text = "Padrão"
    ET.SubElement(cal, "IsBaseCalendar").text = "1"

    # Ordena por dependência já resolvida (start_day) para gerar um outline coerente
    ordered_tasks = sorted(
        project.tasks.values(), key=lambda t: (t.start_day or 0, t.id)
    )
    task_uid_by_id = {t.id: str(i + 1) for i, t in enumerate(ordered_tasks)}

    tasks_el = ET.SubElement(root, "Tasks")
    for i, task in enumerate(ordered_tasks):
        uid = task_uid_by_id[task.id]
        t_start, t_finish = task_calendar_dates(project, task)

        task_el = ET.SubElement(tasks_el, "Task")
        ET.SubElement(task_el, "UID").text = uid
        ET.SubElement(task_el, "ID").text = str(i + 1)
        ET.SubElement(task_el, "Name").text = task.name
        ET.SubElement(task_el, "OutlineLevel").text = "1"
        ET.SubElement(task_el, "Milestone").text = "1" if task.milestone else "0"
        ET.SubElement(task_el, "Duration").text = _duration_iso(
            task.computed_duration_days or 0.0
        )
        ET.SubElement(task_el, "DurationFormat").text = "7"  # dias
        ET.SubElement(task_el, "Start").text = _dt(t_start)
        ET.SubElement(task_el, "Finish").text = _dt(t_finish)
        if task.quantity is not None:
            ET.SubElement(task_el, "Notes").text = (
                f"Quantidade: {task.quantity} {task.unit}; "
                f"Produtividade: {task.productivity_rate} {task.unit}/recurso/dia"
            )

        for pred_id in task.predecessors:
            link = ET.SubElement(task_el, "PredecessorLink")
            ET.SubElement(link, "PredecessorUID").text = task_uid_by_id[pred_id]
            ET.SubElement(link, "Type").text = "1"  # Finish-to-Start

    resource_uid_by_id = {rid: str(i + 1) for i, rid in enumerate(project.resources)}
    resources_el = ET.SubElement(root, "Resources")
    for rid, resource in project.resources.items():
        res_el = ET.SubElement(resources_el, "Resource")
        ET.SubElement(res_el, "UID").text = resource_uid_by_id[rid]
        ET.SubElement(res_el, "Name").text = resource.name
        ET.SubElement(res_el, "Group").text = resource.role
        ET.SubElement(res_el, "StandardRate").text = f"{resource.cost_per_hour}/h"

    assignments_el = ET.SubElement(root, "Assignments")
    assign_uid = 1
    for task in ordered_tasks:
        for rid in task.resource_ids:
            if rid not in resource_uid_by_id:
                continue
            assign_el = ET.SubElement(assignments_el, "Assignment")
            ET.SubElement(assign_el, "UID").text = str(assign_uid)
            ET.SubElement(assign_el, "TaskUID").text = task_uid_by_id[task.id]
            ET.SubElement(assign_el, "ResourceUID").text = resource_uid_by_id[rid]
            assign_uid += 1

    rough = ET.tostring(root, encoding="unicode")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def export_to_msproject_xml(project: Project, filepath: str) -> str:
    xml_str = build_msproject_xml(project)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_str)
    return filepath
