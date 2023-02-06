# Renato Dias
# Nmec: 98380

import logging
import random

import networkx as nx
import time
from matplotlib import colors as mcolors
from random import seed, shuffle
import numpy as np
import itertools as it

class ChromaticNumber_Calc:
    """
	This class finds the chromatic number of a given Graph object.
	"""
    def __init__(self):
        self.seed = 98380
        self.colors = list(mcolors.CSS4_COLORS.values())
        seed(self.seed)
        np.random.seed(self.seed)
        np.random.shuffle(self.colors)

    def node_connectivity(self, nodes, edges):
        #num_edges = len(edges)
        #num_nodes = len(nodes)
        #print(edges)
        #print(nodes)seed
        adjacent_nodes = {node: set() for node in nodes}
        # only go through like the top side of a matrix above diagonal
        for n in nodes:
            for e in edges:
                if e[0] == n:
                    adjacent_nodes[n].add(e[1])
                if e[1] == n:
                    adjacent_nodes[n].add(e[0])
    
        #print(adjacent_nodes)
        return adjacent_nodes

    def randomized_coloring(self, G):
        basic_operations = 0
        total_config_searchs = 0

        start_time = time.time()

        nodes = list(G.nodes())
        edges = list(G.edges())

        # Create a list to store colored nodes
        colored_nodes = []

        # Create a list to store used colors
        used_colors = []

        # Create a list with a number of colors equals to the number of nodes of the graph
        colors = set()

        #Create a temporary list to check adjacent colors
        temp_colors = []

        for i in range(len(nodes)):
            random_color = random.choice(self.colors)
            colors.add(random_color)
            self.colors.remove(random_color)
            basic_operations += 1

        #Replace colors in self.colors list
        for color in colors:
            self.colors.append(color)

        # Create a dictionary that stores the colors
        # initializing all nodes with color 0    
        nodes_colors = {node: -1 for node in nodes}

        # get nodes adjacency dict
        node_adj = self.node_connectivity(nodes, edges)
        basic_operations += 1

        for i in range (len(nodes)):

            n = random.choice(nodes)

            if len(colored_nodes) > 0:
                for node in colored_nodes:
                    if n in node_adj[node]:
                        if nodes_colors[node] in colors:
                            temp_colors.append(nodes_colors[node])
                            colors.remove(nodes_colors[node])
                            basic_operations += 1
                    elif n not in node_adj[node]:
                        if nodes_colors[node] not in colors or nodes_colors[node] not in temp_colors:
                            colors.add(nodes_colors[node])
                            basic_operations += 1
                
            c = random.choice(tuple(colors))
            nodes_colors[n] = c
            nodes.remove(n)
            colored_nodes.append(n)
            colors.remove(c)
            basic_operations += 1
            if c not in used_colors:
                used_colors.append(c)
                basic_operations += 1

        total_config_searchs += 1

        chromatic_number = len(used_colors)

        total_time = time.time() - start_time

        nx.set_node_attributes(G,
            {node: color for node, color in nodes_colors.items()},
            'color')
            
        return chromatic_number, G, total_time, basic_operations, total_config_searchs

