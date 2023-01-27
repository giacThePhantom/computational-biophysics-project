import re
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
import utility as ut
import matplotlib as mpl
import seaborn as sns

def potential_during_em(filename = ut.potential , outname = ut.potential_out, show = False):
    ut.plot_xvg(filename, "Potential during energy minimization", "Time", "Potential (kJ/Mol)", "Potential energy", color = 'blue')
    ut.show_or_save(outname, show)

def temperature_nvt(filename = ut.temperature, outname = ut.temperature_out, show = False):
    ut.plot_xvg(filename, "Temperature during NVT", "Time", "Temperature (K)", "Temperature", color = 'red')
    ut.show_or_save(outname, show)

def pressure_npt(filename = ut.pressure, outname = ut.pressure_out, show = False):
    ut.plot_xvg(filename, "Pressure during NPT", "Time", "Pressure (bar)", "Pressure", color='green')
    ut.show_or_save(outname, show)

def volume_npt(filename = ut.volume, outname = ut.volume_out, show = False):
    ut.plot_xvg(filename, "Volume during NPT", "Time", "Volume (nm^3)", "Volume", color='blue')
    ut.show_or_save(outname, show)

def all_to_all_rmsd(filename = ut.rmsd, outname = ut.all_to_all_rmsd, show = False):
    rmsd_data, dim = ut.read_rmsd_data(filename)
    rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
    plt.figure()
    plt.title("RMSD heatmap", fontsize=20)
    img = plt.imshow(rmsd_map, cmap = 'bwr')
    res = plt.colorbar(img);
    ut.show_or_save(outname, show)

def rmsd(filename = ut.rmsd, outname = ut.rmsd_single, ref = 50, show = False):
    rmsd_data, dim = ut.read_rmsd_data(filename)
    data = list(rmsd_data.loc[rmsd_data[0] == ref][2])
    plt.figure()
    plt.title("RMSD", fontsize=20)
    img = plt.plot(data)
    ut.show_or_save(outname, show)

def radius_of_gyration(filename = ut.rgyr , outname = ut.rgyr_out, show = False):
    rgyr_data = pd.read_csv(filename, header = None)
    plt.title("$R_{g}$",fontsize=16)
    plt.xlabel("ns",fontsize=12)
    plt.ylabel("$A$",fontsize=12)
    res = plt.plot(rgyr_data[0])
    ut.show_or_save(outname, show)

def rmsf(filename = ut.rmsf, outname = ut.rmsf_out, show =False):
    rmsf_data = pd.read_csv(filename, sep = ' ',header = None).T
    plt.plot(rmsf_data)
    plt.xlabel('Residue index')
    plt.ylabel('RMSF')
    plt.title('RMSF')
    plt.axvspan(39, 51, color= 'r', alpha = 0.3)
    plt.axvspan(21, 29, color= 'r', alpha = 0.3)
    plt.axvspan(118, 119, color= 'r', alpha = 0.3)
    plt.axvspan(141, 145, color= 'r', alpha = 0.3)
    plt.axvspan(163, 166, color= 'r', alpha = 0.3)
    plt.axvspan(187, 190, color= 'r', alpha = 0.3)
    plt.axvspan(447, 451, color= 'g', alpha = 0.3)
    plt.axvspan(469, 481, color= 'g', alpha = 0.3)
    plt.axvspan(492, 504, color= 'g', alpha = 0.3)
    plt.axvspan(328, 333, color= 'g', alpha = 0.3)
    plt.axvspan(345, 356, color= 'g', alpha = 0.3)
    plt.axvspan(391, 392, color= 'g', alpha = 0.3)
    ut.show_or_save(outname, show)

def contact_map(gro = ut.gro, xtc = ut.xtc, outname = ut.contact_map_out, sel = "name CA", show = False):
    traj = mda.Universe(gro, xtc)
    atom_selection = traj.select_atoms(sel)
    d_atoms_sel = distances.distance_array(atom_selection.positions, atom_selection.positions)
    plt.title("Contact map")
    img = plt.imshow(d_atoms_sel)
    plt.colorbar(img)



    ut.show_or_save(outname, show)

def clustering(filename = ut.rmsd, outname = ut.clustering_out, linkage_method = 'average', show = False, skip_frames = 0):
    rmsd_data = pd.read_csv(filename, sep=',', header = None)
    rmsd_data.drop(rmsd_data[rmsd_data[0] < skip_frames].index, inplace = True)
    rmsd_data.drop(rmsd_data[rmsd_data[1] < skip_frames].index, inplace = True)
    rmsd_data[0] -= skip_frames
    rmsd_data[1] -= skip_frames
    dim = max(rmsd_data[1])+1
    rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
    Z = linkage(rmsd_map, linkage_method)
    dn = dendrogram(Z,
                    truncate_mode = 'lastp',
                    p=200,  # show only the last p merged clusters
                    leaf_rotation=90.,
                    leaf_font_size=9.,
                    show_contracted=True,
                    )
    ut.show_or_save(outname, show)

def block_analysis(filename = ut.rmsd, outname = ut.block_analysis_out, increase = 5, ds = 5, ref = 40, deleted_frames = 20, show = False):
    data = pd.read_csv(filename, sep = ",", header = None)
    data = data.loc[(data[0] >= deleted_frames) & (data[1] >= deleted_frames)]
    data[0] -= deleted_frames
    data[1] -= deleted_frames
    dim = max(data[1]) + 1
    dim_block = 0
    bse = []
    correlation_time = []
    while dim_block <= dim/2:
        dim_block += increase
        nblocks = int(np.ceil(dim/dim_block))
        means = []
        for i in range(nblocks):
            block = data.loc[(data[0] > (i*dim_block)) &
                            (data[0] <= min((i+1)*dim_block, dim)) &
                            (data[1] == ref) &
                             data[2] != 0]
            if len(block) != 0:
                means.append(np.mean(block.iloc[:,2]))
            else:
                nblocks -=1
        bse.append(np.std(means)/np.sqrt(nblocks))
        print(bse[-1])
        correlation_time.append(dim_block)
    plt.ylabel("BSE")
    plt.xlabel("Block dimension")
    plt.title("Block analysis")
    plt.plot(correlation_time, bse)
    ut.show_or_save(outname, show)

def autocorr_analysis(filename = ut.rmsd, outname = ut.corr_analysis_out, limit=2, ref = 10, show = False):
    data, dim = ut.read_rmsd_data(filename)
    data.drop(data[data[0] != ref].index, inplace = True)
    data = np.array(data[2])
    mean = np.mean(data)
    std = np.std(data)
    N = len(data)
    tp = 0
    tp_arr = []
    C = np.zeros(np.int(N/limit)+1)
    for tp in range(0, np.int(N/limit)+1):
        a = 0
        tp_arr.append(tp)
        for j in range(1, N-tp):
            a += (data[j] - mean)*(data[j+tp]-mean)
        C[tp] = a/(N*(std**2))
    tau = 1+2*np.sum(C)
    N_ind = np.int(N/(2*tau))
    SE_data = std/np.sqrt(N_ind)
    plt.plot(tp_arr, C)
    plt.title("Autocorrelation between frames at distance t")
    plt.xlabel("t'")
    plt.ylabel("C_RMSD [t']")
    plt.axvline(x = tau, color = 'r', label = 'autocorrelation time')
    plt.annotate("Autocorrelation time: {}\nIndependent frames: {}\nStandard deviation: {}".format(tau, N_ind, SE_data), xy = (0.55, 0.75), bbox = dict(facecolor = 'white', alpha = 0.5), xycoords = 'axes fraction')
    plt.legend(loc = 'upper right')
    ut.show_or_save(outname, show)
    return N_ind,SE_data
