import sys
import argparse
import logging
from generate_graphs import Graph_Manager
from chromaticNumber_calc import ChromaticNumber_Calc
import networkx as nx

class Main:
	def __init__(self):
		self.num_nodes, self.generate, self.show_graph, self.exhaustive,\
			self.greedy, self.order_degree_heur, self.vizing_theorem, self.recoloring = self.check_arguments()
		
		self.graph_manager = Graph_Manager()
		self.cn_calculator = ChromaticNumber_Calc()

		self.handle_args()


	def usage(self):
		print("Usage: python3 main.py\
			\n\t-h <Shows available arguments>\
			\n\t-n <Number of Nodes for the Graph to be used for any operation: int>\
			\n\t-ge <Generate Graph>\
			\n\t-e <Exhaustive M-coloring Search>\
			\n\t-gr <Greedy Search>\
			\n\t-s <Show plot of graphs>")
		sys.exit()


	def check_arguments(self):
		arg_parser = argparse.ArgumentParser(
			prog="Vertice Coloring",
			usage=self.usage
		)
		arg_parser.add_argument('-help', action='store_true')
		arg_parser.add_argument('-num_nodes', nargs=1, type=int, default=[40])
		arg_parser.add_argument('-generate', action='store_true')
		arg_parser.add_argument('-greedy', action='store_true')
		arg_parser.add_argument('-exhaustive', action='store_true')
		arg_parser.add_argument('-show_graph', action='store_true')

		try:
			args = arg_parser.parse_args()
		except:
			self.usage()

		if args.help:
			self.usage()

		return args.num_nodes[0], args.generate, args.show_graph,\
				args.exhaustive, args.greedy, args.order_degree_heur,\
				args.vizing_theorem, args.recoloring[0]


	def handle_args(self):
		G = None
		if self.generate:
			G = self.graph_manager.generate(self.num_nodes)
			if self.show_graph:
				self.graph_manager.show_graph(G)
		if not G:
			G = self.graph_manager.load_graph(self.num_nodes)

		if self.exhaustive:
			self.handle_results(*self.cn_calculator.exhaustive_coloring(G, self.vizing_theorem),\
				"Exhaustive" + ('_Vizing' if self.vizing_theorem else ''))

		if self.greedy:
			self.handle_results(*self.cn_calculator.greedy_coloring(G, self.order_degree_heur, self.recoloring),\
				"Greedy" + ('_Heuristic' if self.order_degree_heur else '') +\
				('_Recolored_{self.recoloring}' if self.recoloring else ''))


	def handle_results(self, cn, colored_G, total_time, basic_operations, total_config_searches, strategy):
		logging.info(f"Graph with {nx.number_of_nodes(colored_G)} nodes and {nx.number_of_edges(colored_G)} edges")
		logging.info(f"Chromatic Number Calculated with {strategy.replace('_', ' ')} search: {cn}")
		logging.info(f"Time to Find: {total_time} seconds")
		logging.info(f"Total Basic Operations: {basic_operations}")
		logging.info(f"Total Configurations Searched: {total_config_searches}")

		# store graph png and txt later on a different dir (colored graphs)

		if self.show_graph:
			self.graph_manager.show_graph(colored_G)
		
		self.graph_manager.save_graph(colored_G, strategy)


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

	main = Main()