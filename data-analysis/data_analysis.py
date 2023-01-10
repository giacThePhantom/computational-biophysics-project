import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from os import fspath
import seaborn as sns
import math
import sys
import pandas as pd
import plotly.express as px
import MDAnalysis as mda
from MDAnalysis.lib import distances
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

def all_to_all_rmsd(filename, outname):
    rmsd_data = pd.read_csv(filename, sep=',', header = None)
    dim = max(rmsd_data[1])+1
    rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
    plt.figure(figsize=((10,10)))
    plt.title("RMSD heatmap", fontsize=20)
    img = plt.imshow(rmsd_map)
    res = plt.colorbar(img, cmap=plt.get_cmap('jet'));
    plt.savefig(outname)
    plt.clf()
    return res

def radius_of_gyration(filename, outname):
    rgyr_data = pd.read_csv(filename, header = None)
    plt.title("$R_{g}$",fontsize=16)
    plt.xlabel("ns",fontsize=12)
    plt.ylabel("$A$",fontsize=12)
    res = plt.plot(rgyr_data[0])
    plt.savefig(outname)
    plt.clf()
    return res

def rmsf(filename, outname):
    rmsf_data = pd.read_csv(filename, sep = ' ',header = None).T
    plt.plot(rmsf_data)
    plt.xlabel('Residue index')
    plt.ylabel('RMSF')
    plt.title('RMSF')
    plt.savefig(outname)
    plt.clf()

def contact_map(gro, xtc, outname, sel = "name CA"):
    traj = mda.Universe(gro, xtc)
    atom_selection = traj.select_atoms(sel)
    d_atoms_sel = distances.distance_array(atom_selection.positions, atom_selection.positions)
    plt.title("Contact map")
    img = plt.imshow(d_atoms_sel)
    plt.colorbar(img)
    plt.savefig(outname)
    plt.clf()

def clustering(filename, outname, linkage_method = 'average'):
    rmsd_data = pd.read_csv(filename, sep=',', header = None)
    dim = max(rmsd_data[1])+1
    rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
    Z = linkage(rmsd_map, linkage_method)
    dn = dendrogram(Z)
    plt.savefig(outname)
    plt.clf()

def block_analysis(filename, outname, increase = 10, ds = 5):
    data = pd.read_csv(filename, sep = ",", header = None)
    dim = max(data[1]) + 1
    dim_block = 0
    bse = []
    correlation_time = []
    while dim_block <= dim/2:
        dim_block += increase
        nblocks = int(np.ceil(dim/dim_block))
        means = []
        for i in range(nblocks):
            block = data.loc[(data[0] >= (i*dim_block)) &
                            (data[0] < (i+1)*dim_block) &
                            (data[1] >= (i*dim_block)) &
                            (data[1] < (i+1)*dim_block) &
                             data[2] != 0]
            if len(block) != 0:
                means.append(np.mean(block.iloc[:,2]))
            else:
                nblocks -=1
        bse.append(np.std(means)/np.sqrt(nblocks))
        correlation_time.append(dim_block * ds)
        plt.ylabel("BSE")
        plt.xlabel("Correlation time")
        plt.title("Block analysis")
        plt.plot(correlation_time, bse)
        plt.savefig(outname)
        plt.clf()
