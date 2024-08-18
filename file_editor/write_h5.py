import sys
import h5py


def write_material_h5(filename: str, material_dictionary: dict):
    file = h5py.File(filename, 'w')
    material_group = file.create_group("Materials")

    for keys, values in material_dictionary.items():
        new_material_group = material_group.create_group(str(values.material_id) + "-" + values.name)
        # new_material_group.attrs = {"Name": values.name,
        #                             "ID": values.material_id,}
        new_material_group.create_dataset("ModulusOfElasticity", data=[values.youngs_modulus])
        new_material_group.create_dataset("PoissonsRatio", data=[values.poissons_ratio])
        new_material_group.create_dataset("YieldStrength", data=[values.yield_strength])
        new_material_group.create_dataset("YieldStrain", data=[values.yield_strain])
        new_material_group.create_dataset("TensileStrength", data=[values.tensile_strength])
        new_material_group.create_dataset("TensileStrain", data=[values.tensile_strain])
        new_material_group.create_dataset("ThermalConductivity", data=[values.thermal_conductivity])

    file.close()

    sys.stdout.write(f"Material data saved to HDF5 file: {filename}\n")
