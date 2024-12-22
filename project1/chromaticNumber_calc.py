# Renato Dias
# Nmec: 98380

import logging

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
        #print(nodes)
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


    def get_available_color(self, current_new_color, used_colors):
        color = min([y for y in range(current_new_color) if y not in used_colors],\
                    default=current_new_color)
        return color


    def assign_color(self, nodes_colors, node, current_new_color, color):
        # assign available color to node
        nodes_colors[node] = color
        
        # if available color is equal to new color,
        # means that the new color has to be used
        if current_new_color == color:
            current_new_color += 1
        
        return nodes_colors, current_new_color


    def greedy_coloring(self, G, order_degree_heur=False, recoloring=0):
        basic_operations = 0
        total_config_searchs = 0

        chromatic_number = float('inf')
        final_node_colors = {}

        start_time = time.time()

        nodes = list(G.nodes())
        edges = list(G.edges())
        nodes_colors = {node: -1 for node in nodes}
        current_new_color = 0

        # get adjacency matrix for nodes and list of ordered nodes descending by their node connectivity
        adjacent_nodes = self.node_connectivity(nodes, edges)
        basic_operations += 1

        # sort by highest node connectivity
        if order_degree_heur:
            ordered_nodes = sorted(nodes, key= lambda x: len(adjacent_nodes[x]), reverse=True)
            basic_operations += 1
        else:
            ordered_nodes = nodes
        
        # recoloring a number of times passed as argument using different orders
        # has default value of zero, which means only colors with one order of nodes
        # else it shuffles the list of nodes and recolors them and stores best solution found
        for n_attempt in range(recoloring + 1):

            ordered_nodes_temp = ordered_nodes.copy()

            if n_attempt != 0:
                shuffle(ordered_nodes_temp)
            
            current_new_color = 0
            nodes_colors = {node: -1 for node in nodes}

            # assign a color to the first node
            highest_conn_node = ordered_nodes_temp.pop(0)
            nodes_colors, current_new_color = \
                self.assign_color(nodes_colors, highest_conn_node, current_new_color, current_new_color)
            basic_operations += 1

            # color nodes starting by the highest adjacent nodes
            for node in ordered_nodes_temp:

                # skip if node has a color already assigned
                if nodes_colors[node] != -1:
                    continue

                # temporary sets to store used colors by adjacent nodes
                # and the adjacent nodes that are uncolored so they can be assigned later
                used_colors = set()
                for e in adjacent_nodes[node]:
                    if nodes_colors[e] != -1:
                        used_colors.add(nodes_colors[e])
                basic_operations += 1

                # get available color for this node
                available_color = self.get_available_color(current_new_color, used_colors)
                basic_operations += 1

                # assign available color to current node
                nodes_colors, current_new_color = \
                    self.assign_color(nodes_colors, node, current_new_color, available_color)
                basic_operations += 1

            total_config_searchs += 1
            
            if current_new_color <= chromatic_number:
                chromatic_number = current_new_color
                final_node_colors = nodes_colors.copy()

        total_time = time.time() - start_time

        # happens for graphs with chromatic numbers bigger than 148
        if chromatic_number <= len(self.colors):
            nx.set_node_attributes(G,
                {node: self.colors[color] for node, color in final_node_colors.items()},
                'color')
    
        return chromatic_number, G, total_time, basic_operations, total_config_searchs


    def m_color_search_backtrack(self, node_adj, m, nodes, nodes_colors,\
                                 node_ind, basic_operations, total_config_searchs):
        # all nodes colored then return
        if node_ind == len(nodes):
            return nodes_colors, basic_operations, total_config_searchs

        node = nodes[node_ind]

        # try different colors for node
        for c in range(m):
            # check if node can be colored with this color
            flag = True
            for adj_node in node_adj[node]:
                if c == nodes_colors[adj_node]:
                    flag = False
                    break
            basic_operations += 1
            if flag:
                # assign color if no conflictions
                nodes_colors[node] = c
                basic_operations += 1

                # recursion to check other nodes
                result_nodes_colors, basic_operations, total_config_searchs =\
                    self.m_color_search_backtrack(node_adj, m, nodes,\
                    nodes_colors, node_ind+1, basic_operations, total_config_searchs)
                total_config_searchs += 1
                if result_nodes_colors:
                    return result_nodes_colors, basic_operations, total_config_searchs
                # if color gives no solution, reset color and backtracks here
                nodes_colors[node] = -1
        total_config_searchs += 1
        return None, basic_operations, total_config_searchs


    def exhaustive_coloring(self, G, vizing_theorem):
        basic_operations = 0
        total_config_searchs = 0

        start_time = time.time()

        nodes = list(G.nodes())
        edges = list(G.edges())

        # Create a dictionary that stores the colors
        # initializing all nodes with color 0    
        nodes_colors = {node: -1 for node in nodes}

        # get nodes adjacency dict
        node_adj = self.node_connectivity(nodes, edges)
        basic_operations += 1

        # Vizing Theorem
        if vizing_theorem:
            highest_edge_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)[0][1]
            m_values = [highest_edge_degree + 1, highest_edge_degree]
            basic_operations += 1
        else:
            m_values = [1]

        while True:
            m = m_values.pop()

            # start search on the first node of index 0
            result_nodes_colors, basic_operations, total_config_searchs =\
                self.m_color_search_backtrack(node_adj, m, nodes, nodes_colors, 0, basic_operations, total_config_searchs)

            if result_nodes_colors:
                nodes_colors = result_nodes_colors
                chromatic_number = m
                break

            if not vizing_theorem:
                m_values.append(m + 1)

        total_time = time.time() - start_time

        nx.set_node_attributes(G,
            {node: self.colors[color] for node, color in nodes_colors.items()},
            'color')
        
        return chromatic_number, G, total_time, basic_operations, total_config_searchs

