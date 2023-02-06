# Renato Dias
# Nmec: 98380

import logging
from random import randint, random, choice, seed
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, groupby, product


class Graph_Manager:
	"""
	This class creates graphs that obey the following rules:
		- vertices are 2D points on the XOY plane, with integer valued
		coordinates between 1 and 9.
		- vertices should neither be coincident nor too close.
		- the number of edges sharing a vertex is randomly determined.
	"""
	def __init__(self):
		self.GRAPH_DIRECTORY = 'graphs/'
		self.COLORED_GRAPH_DIRECTORY = 'colored_graphs/'
		self.SEED = 98380
		
		# Sets grid behind all graph elements for better plot view experience
		plt.rc('axes', axisbelow=True)


	def generate(self, num_nodes):
		"""
		Generates a random undirected graph, similarly to an Erdős-Rényi 
		graph, but enforcing that the resulting graph is conneted
		"""
		assert num_nodes > 1, "Can only generate graphs that have more than 2 nodes"
		
		int_positions = True
		if num_nodes > 81:
			logging.info("Positions for graphs that have more than 81 nodes are "
		 		"random since with 2D integer coordinates from 1 to 9, "
				"it can only fit 81 nodes in the coordinates grid")
			int_positions = False

		seed(self.SEED)

		edge_prob = random()
		all_possible_edges = combinations(range(num_nodes), 2)

		G = nx.Graph()
		G.add_nodes_from(range(num_nodes))

		if edge_prob <= 0:
			return G
		if edge_prob >= 1:
			return nx.complete_graph(G.nodes(), create_using=G)
		for _, node_edges in groupby(all_possible_edges, key=lambda x: x[0]):
			node_edges = list(node_edges)
			random_edge = choice(node_edges)
			G.add_edge(*random_edge)
			for e in node_edges:
				if random() < edge_prob:
					G.add_edge(*e)

		if int_positions:
			node_positions = nx.spring_layout(G, k=2, scale=4, center=(5,5), seed=self.SEED)
			positions = { node: (int(pos[0]), int(pos[1])) for node, pos in node_positions.items() }

			all_possible_coords = [x for x in product((1,2,3,4,5,6,7,8,9), repeat=2) if x not in positions.values()]
			for n1 in sorted(positions.keys()):
				for n2 in sorted(positions.keys()):
					if n1 != n2 and positions[n1] == positions[n2]:
						rand_index = randint(0, len(all_possible_coords)-1)
						new_pos = all_possible_coords[rand_index]
						del all_possible_coords[rand_index]
						positions[n2] = new_pos
		else:
			# this will generate positins from -1 to 1
			# with each position as a float
			# this is only used for testing purposes of very large graphs
			# which will allow nodes on very close positions
			positions = { node: (pos[0], pos[1]) for node, pos\
				in nx.spring_layout(G, k=2, seed=self.SEED).items() }

		nx.set_node_attributes(G, positions, 'pos')

		# undirected because for the given problem edges directions do not matter
		# if the graphs are directed, the chromatic index will still
		# be calculated but as if each edge represents two edges, one for each direction
		G = nx.to_undirected(G)

		logging.info(f"Generated Connected Graph with {num_nodes} vertices and {nx.number_of_edges(G)} edges, probability of edges {edge_prob}")

		self.save_graph(G)
	
		return G


	def show_graph(self, G):
		#edge_positions = nx.get_edge_attributes(G, 'pos')
		node_positions = nx.get_node_attributes(G, 'pos')
		node_colors = nx.get_node_attributes(G, 'color').values()
		if not node_colors:
			node_colors = 'g'

		fig, ax = plt.subplots()
		fig.set_size_inches(8.5, 8.5)

		nx.draw(G, node_positions, node_color=node_colors,\
			with_labels=True, font_weight='bold', ax=ax,\
			node_size=400, font_size=8)

		if type(node_positions[0][0]) == int:
			plt.axis('on')
			plt.xticks([1,2,3,4,5,6,7,8,9])
			plt.yticks([1,2,3,4,5,6,7,8,9])
			ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
			plt.grid()
		plt.show()
		plt.clf()
		plt.cla()
		plt.close()


	def save_graph(self, G, strategy=None, num_Attemp=0):
		num_nodes = G.number_of_nodes()
		
		node_positions = nx.get_node_attributes(G, 'pos')
		node_colors = nx.get_node_attributes(G, 'color').values()
		if not node_colors:
			node_colors = 'g'

		fig, ax = plt.subplots()
		fig.set_size_inches(8.5, 8.5)

		nx.draw(G, node_positions, node_color=node_colors,\
			with_labels=True, font_weight='bold', ax=ax,\
			node_size=400, font_size=8)

		if type(node_positions[0][0]) == int:
			plt.axis('on')
			plt.xticks([1,2,3,4,5,6,7,8,9])
			plt.yticks([1,2,3,4,5,6,7,8,9])
			ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
			plt.grid()
		
		logging.info("Saving graph to file")

		if not strategy:
			plt.savefig(f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}_Attempt_{num_Attemp}.png", bbox_inches='tight')
			nx.write_gml(G, f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}.txt")
		else:
			plt.savefig(f"{self.COLORED_GRAPH_DIRECTORY}{strategy}_Colored_Graph_{num_nodes}_Attempt_{num_Attemp}.png", bbox_inches='tight')
			
		plt.clf()
		plt.cla()
		plt.close()



	def load_graph(self, num_nodes):
		try:
			logging.info(f"Retrieving graph from saved files")
			G = nx.read_gml(f"{self.GRAPH_DIRECTORY}Graph_{num_nodes}.txt")
			nodes_to_int = {n:int(n) for n in G.nodes()}
			return nx.relabel_nodes(G, nodes_to_int, copy=True)
		except FileNotFoundError:
			logging.info(f"Didn't found a graph saved with this number of nodes, generating one instead")
			return self.generate(num_nodes)