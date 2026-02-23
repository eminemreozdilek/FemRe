import pyvista as pv
from dataclasses import dataclass
from model.material import BaseMaterial


@dataclass
class ComponentData:
    component_id: int
    name: str
    mesh: pv.UnstructuredGrid
    material: BaseMaterial
