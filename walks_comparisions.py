# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:43:27 2020

@author: Giovanni G Soares
"""

import igraph as gr
import matplotlib.pyplot as plt
import numpy as np

# random.seed(8666)
font = {'family' : 'Arial',
        'weight' : 'bold',
        'size'   : 22}
plt.rc('text', usetex=True)
plt.rc('font', **font)

G = gr.Graph.Famous("zachary")

X= G.get_adjacency(2).data
AUX = np.copy(X)
qtd = 100000
steps = 12
i = steps
for i in range(2, steps+1):
    print(i)
    XX = np.zeros((G.vcount(), G.vcount()))
    for j in range(G.vcount()):
        for k in range(qtd):
            walk = G.random_walk(j, i)
            XX[j][walk[-1]] += 1/qtd
    plt.figure(figsize = (15, 10))
    plt.subplot(2, 2, 1)
    plt.title(f"Walk: {i-1} steps")
    plt.imshow(XX, alpha=0.8, cmap='inferno')
    plt.colorbar()
    plt.subplot(2, 2, 2)
    plt.title("Matrix: $A^{{{}}}$".format(i-1))
    plt.imshow(AUX, alpha=0.8, cmap='inferno')
    plt.colorbar()
    plt.savefig("matrixes_" + str(i-1) +".png")
    list_simu = []
    list_mat = []
    for ii in range(G.vcount()):
        for jj in range(G.vcount()):
            list_mat.append(AUX[ii][jj])
            list_simu.append(XX[ii][jj])
    plt.figure(figsize = (10,10))
    plt.title(f"Scatter plot of walks probability x possible walks for\n {i-1} steps")
    plt.xlabel("Adjacency matrix: total of possible walks")
    plt.ylabel("Simulated walk: probability")
    plt.plot(list_mat, list_simu, 'o')
    plt.savefig("scatter_" + str(i-1) +".png")
    AUX = np.matmul(AUX, X)


# plt.imshow(AUX, alpha=0.8, cmap='inferno')
# plt.colorbar()
# plt.savefig("matrixes_" + str(i) +".png")
# AUX = np.matmul(AUX, X)


