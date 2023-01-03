import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from os import fspath
import seaborn as sns
import math
import sys
import pandas as pd

rmsd_data = pd.read_csv(sys.argv[1], sep=',', header = None)

dim = max(rmsd_data[1])+1

rmsd_map = np.array(rmsd_data[2]).reshape((dim,dim))
plt.figure(figsize=((10,10)))
plt.title("RMSD heatmap", fontsize=20)
img = plt.imshow(rmsd_map)
plt.colorbar(img, cmap=plt.get_cmap('jet'));
plt.show()
