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


def get_pocket_persitence(data, threshold = 0):
    temp = data.sum() / len(data)
    pocket = []
    for i in temp.index:
        if temp[i] > threshold:
            pocket.append(i)

    return pocket



# Ligand exiting for second chain 0:4000 - 4100:4400 - 4400:4660

# Step first chain 0:1240 - 1240:1400 - 1400:1460

data = pd.read_csv(sys.argv[1])
data = data.iloc[: , 1:]
data = data.iloc[1:, :]

first_pocket = get_pocket_persitence(data.iloc[:4000,:], 0.7)
second_pocket = get_pocket_persitence(data.iloc[4000:4400,:], 0.7)
third_pocket = get_pocket_persitence(data.iloc[4400:4660,:], 0.7)
all_res = set(first_pocket).union(set(second_pocket), set(third_pocket))
res = pd.DataFrame(False, index = all_res, columns = ["0:4000", "4000:4400", "4400:4660"])
for i in first_pocket:
    res["0:4000"][i] = True

for i in second_pocket:
    res["4000:4400"][i] = True

for i in third_pocket:
    res["4400:4660"][i] = True

res.to_csv(sys.argv[3])
print(res)

temp = all_res
data = pd.read_csv(sys.argv[2])
data = data.iloc[: , 1:]
data = data.iloc[1:, :]

first_pocket = get_pocket_persitence(data.iloc[:1240,:], 0.7)
second_pocket = get_pocket_persitence(data.iloc[1240:1400,:], 0.7)
third_pocket = get_pocket_persitence(data.iloc[1400:1460,:], 0.7)
all_res = set(first_pocket).union(set(second_pocket), set(third_pocket))
res = pd.DataFrame(False, index = all_res, columns = ["0:1240", "1240:1400", "1400:1460"])
for i in first_pocket:
    res["0:1240"][i] = True

for i in second_pocket:
    res["1240:1400"][i] = True

for i in third_pocket:
    res["1400:1460"][i] = True

res.to_csv(sys.argv[4])
print(res)
