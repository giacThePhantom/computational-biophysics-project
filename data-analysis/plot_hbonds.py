import matplotlib.pyplot as plt
import numpy as np
import pathlib
import os
import utility as ut
import sys




def hbonds(filename, show = False, min_frame = 0, max_frame = 8001):
    x = []
    y = []
    with open(filename) as f:
        for line in f:
            if line[0] != '#' and line[0] != '@':
                cols = line.split()
                if len(cols) == 2 and float(cols[0]) >= min_frame and float(cols[0]) <= max_frame:
                    x.append(float(cols[0]))
                    y.append(float(cols[1]))
    name = filename.split('/')[-1].split('.')[0]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(min_frame, max_frame)
    ax1.set_title(name)
    ax1.set_xlabel("Time (ns)")
    ax1.set_ylabel("Hydrogen bonds")
    ax1.plot(x,y, c="b")
    print(np.arange(min_frame, max_frame, 1000))
    ax1.set_xticks(np.arange(min_frame, max_frame, 1000))
    ax1.set_xticklabels(np.arange(min_frame / 20, max_frame/20, 50))
    leg = ax1.legend()
    ut.show_or_save(name + '.png', show)


amino_acid_pair = sys.argv[1]
ligand_amino_acids = sys.argv[2]

hbonds(amino_acid_pair)
hbonds(ligand_amino_acids, min_frame = 4500, max_frame = 7000)
