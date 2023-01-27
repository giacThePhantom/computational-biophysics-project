import pandas as pd
import numpy as np
import sys
from subprocess import Popen, PIPE, CalledProcessError, DEVNULL

def read_gro(gro_file):
    first_chain = []
    second_chain = []
    with open(gro_file, 'r') as gro:
        i = 0

        #atom id colum 15-22
        #resname col 0-11
        for line in gro:
            if i >=2 and i < 4688:
                first_chain.append([line[0:11].replace(" ", ""), int(line[15:22])])
            elif i >= 2 and i > 4807 and i < 9495:
                second_chain.append([line[0:11].replace(" ", ""), int(line[15:22])])
            i += 1
    return first_chain, second_chain

def create_matrix(chain, n_frames):
    residue_list = pd.unique([x[0] for x in chain])
    res = np.zeros(shape = (n_frames, len(residue_list)))
    res = pd.DataFrame(res, columns = residue_list)
    return res

def get_residue_from_atom_number(residue, first_chain, second_chain):
    res = []
    for i in first_chain:
        if residue == i[1]:
            res = [1, i[0]]
    for i in second_chain:
        if residue == i[1]:
            res = [2, i[0]]
    return res

def add_frame_information(matrix_first_chain, matrix_second_chain, first_chain, second_chain, i, atoms):
    for atom in atoms.split():
        resid = get_residue_from_atom_number(int(atom)+1, first_chain, second_chain)
        if resid[0] == 1:
            matrix_first_chain[resid[1]][i-1] = 1
        elif resid[0] == 2:
            matrix_second_chain[resid[1]][i-1] = 1

first_chain, second_chain = read_gro(sys.argv[1])
matrix_first_chain = None
matrix_second_chain = None


cmd = f'vmd {sys.argv[1]} {sys.argv[2]} -dispdev text -eofexit -args {sys.argv[6]} < {sys.argv[3]}'

with Popen(cmd, stdout=PIPE,  stderr=DEVNULL, bufsize=1, universal_newlines=True, shell = True) as p:
    i = 0
    for line in p.stdout:
        if 'Info' not in line and 'Warning' not in line and 'atomselect' not in line and 'argv' not in line and 'csv' not in line and i > 0:
            add_frame_information(matrix_first_chain, matrix_second_chain, first_chain, second_chain, i, line)
            i += 1
        if 'Info' not in line and 'Warning' not in line and 'atomselect' not in line and 'argv' not in line and i == 0:
            matrix_first_chain = create_matrix(first_chain, int(line))
            matrix_second_chain = create_matrix(second_chain, int(line))
            i += 1

if p.returncode != 0:
    raise CalledProcessError(p.returncode, p.args)

matrix_first_chain.to_csv(sys.argv[4])
matrix_second_chain.to_csv(sys.argv[5])
