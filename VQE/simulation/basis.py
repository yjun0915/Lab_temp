import numpy as np
import matplotlib.pyplot as plt
from openfermion.chem import MolecularData
from openfermion.transforms import get_fermion_operator, jordan_wigner, bravyi_kitaev
from openfermion.linalg import get_sparse_operator
from openfermionpyscf import run_pyscf

#define constants
basis = "sto-3g"  #basis set
multiplicity = 2  #spin multiplicity
charge = 0        #total charge for the molecule
distance = 0.05
geometry = [("He",(0,0,0)),("H", (0,0,distance))]  #xyz coordinates for atoms
description = str(distance)  #description for the psi4 output file

molecule = MolecularData(geometry, basis, multiplicity, charge, description)
print(molecule)

molecule = run_pyscf(molecule,run_scf=1,run_fci=1)

jw_hamiltonian = jordan_wigner(get_fermion_operator(molecule.get_molecular_hamiltonian()))

print(jw_hamiltonian)
jw_matrix = get_sparse_operator(jw_hamiltonian)
