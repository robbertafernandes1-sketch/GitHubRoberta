import xml.etree.ElementTree as ET

from agente_planejador_ms_project.models import Project, Resource, Task
from agente_planejador_ms_project.msproject_export import MS_PROJECT_NS, build_msproject_xml, export_to_msproject_xml

NS = {"mp": MS_PROJECT_NS}


def _sample_project() -> Project:
    project = Project(name="Obra X", start_date="2026-01-05", skip_weekends=False)
    project.resources["pedreiro"] = Resource(id="pedreiro", name="Pedreiro", cost_per_hour=25.0)
    project.tasks["fundacao"] = Task(
        id="fundacao", name="Fundação", quantity=40, unit="m3", productivity_rate=10,
        resource_ids=["pedreiro"],
    )
    project.tasks["alvenaria"] = Task(
        id="alvenaria", name="Alvenaria", quantity=100, unit="m2", productivity_rate=20,
        resource_ids=["pedreiro"], predecessors=["fundacao"],
    )
    return project


def test_build_xml_has_expected_structure():
    project = _sample_project()
    xml_str = build_msproject_xml(project)
    root = ET.fromstring(xml_str)

    assert root.tag == f"{{{MS_PROJECT_NS}}}Project"
    assert root.find("mp:Name", NS).text == "Obra X"

    tasks = root.findall("mp:Tasks/mp:Task", NS)
    assert len(tasks) == 2
    names = {t.find("mp:Name", NS).text for t in tasks}
    assert names == {"Fundação", "Alvenaria"}

    resources = root.findall("mp:Resources/mp:Resource", NS)
    assert len(resources) == 1
    assert resources[0].find("mp:Name", NS).text == "Pedreiro"

    assignments = root.findall("mp:Assignments/mp:Assignment", NS)
    assert len(assignments) == 2


def test_second_task_has_predecessor_link():
    project = _sample_project()
    xml_str = build_msproject_xml(project)
    root = ET.fromstring(xml_str)

    alvenaria = next(
        t for t in root.findall("mp:Tasks/mp:Task", NS)
        if t.find("mp:Name", NS).text == "Alvenaria"
    )
    links = alvenaria.findall("mp:PredecessorLink", NS)
    assert len(links) == 1


def test_duration_iso_format_present():
    project = _sample_project()
    xml_str = build_msproject_xml(project)
    root = ET.fromstring(xml_str)
    for task in root.findall("mp:Tasks/mp:Task", NS):
        duration = task.find("mp:Duration", NS).text
        assert duration.startswith("PT")
        assert duration.endswith("S")


def test_export_writes_file(tmp_path):
    project = _sample_project()
    filepath = tmp_path / "plano.xml"
    result = export_to_msproject_xml(project, str(filepath))
    assert result == str(filepath)
    assert filepath.exists()
    content = filepath.read_text(encoding="utf-8")
    assert "Obra X" in content
