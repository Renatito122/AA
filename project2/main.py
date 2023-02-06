import sys
import argparse
import logging
from generate_graphs import Graph_Manager
from chromaticNumber_calc import ChromaticNumber_Calc
import networkx as nx

class Main:
	def __init__(self):
		self.num_nodes, self.generate, self.show_graph,\
			self.randomized = self.check_arguments()
		
		self.graph_manager = Graph_Manager()
		self.cn_calculator = ChromaticNumber_Calc()

		self.handle_args()


	def usage(self):
		print("Usage: python3 main.py\
			\n\t-h <Shows available arguments>\
			\n\t-n <Number of Nodes for the Graph to be used for any operation: int>\
			\n\t-ge <Generate Graph>\
			\n\t-r <Randomized Coloring>\
			\n\t-s <Show plot of graphs>")
		sys.exit()


	def check_arguments(self):
		arg_parser = argparse.ArgumentParser(
			prog="Vertice Coloring",
			usage=self.usage
		)
		arg_parser.add_argument('-help', action='store_true')
		arg_parser.add_argument('-num_nodes', nargs=1, type=int, default=[139])
		arg_parser.add_argument('-generate', action='store_true')
		arg_parser.add_argument('-show_graph', action='store_true')
		arg_parser.add_argument('-randomized', action='store_true')


		try:
			args = arg_parser.parse_args()
		except:
			self.usage()

		if args.help:
			self.usage()

		return args.num_nodes[0], args.generate, args.show_graph,\
				args.randomized


	def handle_args(self):
		G = None
		best_cn = 1000
		if self.generate:
			G = self.graph_manager.generate(self.num_nodes)
			if self.show_graph:
				self.graph_manager.show_graph(G)
		if not G:
			G = self.graph_manager.load_graph(self.num_nodes)

		if self.randomized:
			for i in range (self.num_nodes):
				best_cn= self.handle_results(*self.cn_calculator.randomized_coloring(G),\
					"Randomized", i, best_cn)

	def handle_results(self, cn, colored_G, total_time, basic_operations, total_config_searches, strategy, i, best_cn):
		logging.info(f"Graph with {nx.number_of_nodes(colored_G)} nodes and {nx.number_of_edges(colored_G)} edges")
		logging.info(f"Chromatic Number Calculated with {strategy.replace('_', ' ')} search: {cn}")
		logging.info(f"Time to Find: {total_time} seconds")
		logging.info(f"Total Basic Operations: {basic_operations}")
		logging.info(f"Total Configurations Searched: {total_config_searches}")
		if best_cn > cn:
			best_cn = cn
		logging.info(f"Best Chromatic Number Calculated: {best_cn}")
		logging.info("--------------------------------------------------------------")
		


		# store graph png and txt later on a different dir (colored graphs)

		if self.show_graph:
			self.graph_manager.show_graph(colored_G)
		
		self.graph_manager.save_graph(colored_G, strategy, i)

		return best_cn


if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

	main = Main()