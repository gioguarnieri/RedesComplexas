# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 08:45:57 2020

@author: Giovanni Guarnieri Soares
"""
import igraph as gr
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import networkx as nx
import random
# 666, 8666
random.seed(8666)


def isolation(g):
    order = g.vcount()
    infinities = []
    for i in range(0, order):
        graph_copy = g.copy()
# will contain the edge's ids (the ones that will be removed)
        del_list = []
        for target_vertex_id in range(0, order):
            try:
                # Gets the id of the edge that belongs to the pair of vertices
                # (i,target_vertex_id) and puts it in 'del_list'
                del_list.append(graph_copy.get_eid(i, target_vertex_id))
            except:
                pass  # in case the id does not exist
        # deletes all edges connected to the node i
        graph_copy.delete_edges(del_list)
        components_sizes = graph_copy.components().sizes()
        count = 0
        # looping through all components and counting unreachable pairs of
        # vertices in newly modified graph
        total = order
        for c in components_sizes:
            total = total - c
            count += 2*c*total
        infinities.append(count)
    return infinities


def global_efficiency(g):
    invcam = 0
    n = g.vcount()
    global_efficiencies = []
    # returns a list with all shortest paths from each vertex
    shortest_paths = g.shortest_paths_dijkstra()
    for vertex_paths in shortest_paths:
        # iterates on each single shortest path
        for shortest_path in vertex_paths:
            if shortest_path != 0:
                # acumulates the efficiency of each pair of nodes
                invcam += 1 / shortest_path
    # Calculates global efficiency
    eg = invcam / (n * (n - 1))
    global_efficiencies.append(eg)
    return eg


def vulnerability(g):
    vulnerabilities = []
    # Eficiencia com o vertice
    eg = global_efficiency(g)
    # Eficiencia sem o vertice
    # iterating for all vertices
    order = g.vcount()
    for i in range(0, order):
        # makes a copy of the original graph
        g2 = g.copy()
# lista que conterá os ids das arestas do vértice 'i' que serão removidas.
        del_list = []
        for target_vertex_id in range(0, order):
            try:
                # Gets the id of the edge that belongs to the pair of
                # vertices(i,target vertex_id) and puts it in 'del_list'
                del_list.append(g2.get_eid(i, target_vertex_id))
            except:
                pass  # In case the id does not exist
        # deletes all edges of connected to the vertex i
        g2.delete_edges(del_list)
        # gets the efficiency
        efi = global_efficiency(g2)
        # calculates vulnerability
        v = (eg - efi) / eg
        vulnerabilities.append(v)
    return vulnerabilities


GR = [gr.Graph.Famous("zachary"), gr.Graph.Watts_Strogatz(1, 34, 1, 0),
      gr.Graph.Watts_Strogatz(1, 34, 2, 0.8)]

have_path = []
for i in range(34):
    for j in range(i+1, 34):
        have_path.append(GR[2].shortest_paths_dijkstra(i, j))
plt.rcParams.update({'font.size': 35})
ii = 0
for g in GR:
    ii += 1
    iso = []
    vul = []
    iso = isolation(g)
    vul1 = vulnerability(g)
    vul = [round(i, 6) for i in vul1]
    g.vs["label"] = range(g.vcount())
    # layout = g.layout("kk")
    # gr.plot(g, "karateclub.png", layout=layout)
    # plt.show()
    convert = g.get_edgelist()
    G = nx.Graph(convert)
    N = g.vcount()
    normiso = [float(i)/(N*(N-1)) for i in iso]
    cmap = plt.cm.rainbow
    facecolor = "gainsboro"
    norm = matplotlib.colors.Normalize(vmin=min(normiso), vmax=max(normiso))
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_facecolor(facecolor)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # only needed for matplotlib < 3.1
    fig.colorbar(sm)
    # plt.title("Isolation")
    fig, ax = plt.subplots(1, 2)
    nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G), cmap='rainbow',
                     node_color=normiso, node_size=30000*np.array(normiso),
                     font_color='black', style='dotted', font_weight='heavy',
                     font_size=35)
    # plt.savefig(f"iso{ii}.pdf")
    cmap = plt.cm.rainbow
    norm = matplotlib.colors.Normalize(vmin=min(vul), vmax=max(vul))
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_facecolor(facecolor)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # only needed for matplotlib < 3.1
    fig.colorbar(sm)
    # plt.title("Vulnerability")
    nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G), cmap='rainbow',
                     node_color=vul, node_size=30000*np.array(vul),
                     font_color='black', style='dotted',
                     font_weight='heavy', font_size=35)
    plt.savefig(f"both{ii}.pdf")
