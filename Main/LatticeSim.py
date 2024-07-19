import numpy as np

def generate_diamond_lattice_atoms(unit_cells):
    atoms = []
    fcc_atoms = [
        [0, 0, 0],
        [0.5, 0.5, 0],
        [0.5, 0, 0.5],
        [0, 0.5, 0.5]
    ]
    basis_atoms = [
        [0.25, 0.25, 0.25],
        [0.75, 0.75, 0.25],
        [0.75, 0.25, 0.75],
        [0.25, 0.75, 0.75]
    ]

    for x in range(unit_cells):
        for y in range(unit_cells):
            for z in range(unit_cells):
                for atom in fcc_atoms:
                    atoms.append([x + atom[0], y + atom[1], z + atom[2]])
                for atom in basis_atoms:
                    atoms.append([x + atom[0], y + atom[1], z + atom[2]])
    
    return np.array(atoms)

# Example usage: Generate atoms in a 2x2x2 unit cell volume
unit_cells = 2
atoms = generate_diamond_lattice_atoms(unit_cells)
print(atoms)
