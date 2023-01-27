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


path = '../../data/8K4D/'

potential = path + 'em_output/potential.xvg'
temperature = path + 'nvt_output/temperature.xvg'
pressure = path + 'npt_output/pressure.xvg'
volume = path + 'npt_output/volume.xvg'
rmsd = path + 'vmd_data/rmsd.csv'
rmsf = path + 'vmd_data/rmsf.csv'
rgyr = path + 'vmd_data/rgyr.csv'
outpath = path + 'data-analysis-output/'
pre_processing =  outpath + 'pre-processing/'
gro = '../../data/8K4D/400ns/md.gro'
xtc = '../../data/8K4D/400ns/md_noPBC.xtc'

potential_out = pre_processing + 'potential.png'
temperature_out = pre_processing + 'temperature.png'
pressure_out = pre_processing + 'pressure.png'
volume_out = pre_processing + 'volume.png'
all_to_all_rmsd = outpath + 'all-to-all-rmsd.png'
rmsd_single = outpath + 'rmsd.png'
rgyr_out = outpath + 'rgyr.png'
rmsf_out = outpath + 'rmsf.png'
contact_map_out = outpath + 'contact-map.png'
clustering_out = outpath + 'clustering.png'
block_analysis_out = outpath + 'block_analysis.png'
corr_analysis_out = outpath + 'autocorrelation-analysis.png'

first_chain = path + '../../data/interactions/binding_pocket_first_chain.csv'
second_chain = path + '../../data/interactions/binding_pocket_second_chain.csv'
first_chain_out = outpath + 'first_chain_proximity.png'
second_chain_out = outpath + 'second_chain_proximity.png'



def plot_xvg(filename, title, xlab, ylab, datalab, color='red'):
    x, y = [], []
    with open(filename) as f:
        for line in f:
            if line[0] != '#' and line[0] != '@':
                cols = line.split()
                if len(cols) == 2:
                    x.append(float(cols[0]))
                    y.append(float(cols[1]))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title(title)
    ax1.set_xlabel(xlab)
    ax1.set_ylabel(ylab)
    ax1.plot(x,y, c=color, label=datalab)
    leg = ax1.legend()

def show_or_save(outname, test):
    if test:
        plt.show()
    else:
        plt.savefig(outname)
    plt.clf()


def read_rmsd_data(filename):
    rmsd_data = pd.read_csv(filename, sep=',', header = None)
    dim = max(rmsd_data[1])+1
    return rmsd_data, dim

def plot_ligand_proximity(chain, out, nchain, show = False):
    chain = pd.read_csv(chain).T
    chain = chain.iloc[1: , :]
    chain = chain.iloc[: , 1:]
    x = []
    y = []
    for i in chain.columns:
        for j in chain.index:
            if chain[i][j] != 0:
                x.append(float(i)/20)
                y.append(int(re.findall(r'\d+', j)[0]))
    if nchain == '1':
        plt.axhspan(39, 51, color= 'r', alpha = 0.3)
        plt.axhspan(21, 29, color= 'r', alpha = 0.3)
        plt.axhspan(118, 119, color= 'r', alpha = 0.3)
        plt.axhspan(141, 145, color= 'r', alpha = 0.3)
        plt.axhspan(163, 166, color= 'r', alpha = 0.3)
        plt.axhspan(187, 190, color= 'r', alpha = 0.3)

    if nchain == '2':
        plt.axhspan(141, 145, color= 'g', alpha = 0.3)
        plt.axhspan(163, 175, color= 'g', alpha = 0.3)
        plt.axhspan(186, 198, color= 'g', alpha = 0.3)
        plt.axhspan(22, 27, color= 'g', alpha = 0.3)
        plt.axhspan(39, 50, color= 'g', alpha = 0.3)
        plt.axhspan(85, 86, color= 'g', alpha = 0.3)
    plt.scatter(x, y, s = 3)
    ut.show_or_save(out, show)
