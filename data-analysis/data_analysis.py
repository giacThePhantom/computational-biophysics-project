import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from os import fspath
import seaborn as sns
import math
import sys
import pandas as pd

def all_to_all_rmsd(filename, outname):
    rmsd_data = pd.read_csv(filename, sep=',', header = None)
    dim = max(rmsd_data[1])+1
    rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
    plt.figure(figsize=((10,10)))
    plt.title("RMSD heatmap", fontsize=20)
    img = plt.imshow(rmsd_map)
    res = plt.colorbar(img, cmap=plt.get_cmap('jet'));
    plt.savefig(outname)
    return res

def radius_of_gyration(filename, outname):
    rgyr_data = pd.read_csv(filename, header = None)
    plt.title("$R_{g}$",fontsize=16)
    plt.xlabel("ns",fontsize=12)
    plt.ylabel("$A$",fontsize=12)
    res = plt.plot(rgyr_data[0])
    plt.savefig(outname)
    return res

def rmsf(filename, outname):
    rmsf_data = pd.read_csv(filename, sep = ' ',header = None).T
    plt.plot(rmsf_data)
    plt.xlabel('Residue index')
    plt.ylabel('RMSF')
    plt.title('RMSF')
    plt.savefig(outname)

# res = all_to_all_rmsd("../../data/data-analysis/rmsd.csv")
# plt.show(res)

# res = radius_of_gyration("../../data/data-analysis/radius-of-gyration.csv")
# plt.show(res)
