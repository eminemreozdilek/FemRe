from preprocessor.properties import material as mtrl
from preprocessor.models import nodes as nd
from preprocessor.models import elements as el


def write_input_lif(file_name: str, nodes: dict, struts: dict, materials: dict):
    file = open(file_name, "w")

    for node in nodes:
        node: nd.Node = nodes[node]
        file.write("Node ")
        file.write(str(node.node_id))
        file.write(" ")
        file.write(str(node.x))
        file.write(" ")
        file.write(str(node.y))
        file.write(" ")
        file.write(str(node.z))
        file.write("\n")

    for strut in struts:
        strut: el.Strut = struts[strut]
        file.write("STRUT ")
        file.write(str(strut.strut_id))
        file.write(" ")
        file.write(str(strut.start_node.node_id))
        file.write(" ")
        file.write(str(strut.end_node.node_id))
        file.write(" ")
        file.write(str(strut.material.material_id))
        file.write(" ")
        file.write(str(strut.radius))
        file.write("\n")

    for material in materials:
        material: mtrl.NonLinearMaterial = materials[material]
        file.write("MAT ")
        file.write(str(material.material_id))
        file.write(" ")
        file.write(str(material.modulus_of_elasticity))
        file.write(" ")
        file.write(str(material.poissons_ratio))
        file.write(" ")
        file.write(str(material.yield_strength))
        file.write(" ")
        file.write(str(material.tensile_strength))
        file.write(" ")
        file.write(str(material.yield_strain))
        file.write(" ")
        file.write(str(material.tensile_strain))
        file.write(" ")
        file.write(str(material.thermal_conductivity))
        file.write("\n")

    file.close()
