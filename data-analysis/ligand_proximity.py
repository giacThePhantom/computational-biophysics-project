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

def ligand_proximity(chain, out, nchain, show = False):
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


ligand_proximity(sys.argv[1], sys.argv[2], sys.argv[3], show = False)
