import sys
import logging
import argparse
from tests import Test


class Main:
    def __init__(self):
        Test(*self.check_arguments())


    def usage(self):
        print("Usage: python3 main.py\
            \n\t-f <File Name for Counting Letters: str>\
            \n\t-k <Top 'k' Most Occurrent Letters: int>\
            \n\t-r <Repetitions for Testing: int>\
            \n\t-l <Epsilon for Lossy Count: float>")

        sys.exit()


    def check_arguments(self):
        arg_parser = argparse.ArgumentParser(
            prog="Approximate Counter",
            usage=self.usage
        )
        arg_parser.add_argument('-help', action='store_true')
        arg_parser.add_argument('-file_name', nargs=1, type=str, default=['datasets/AssociationFootball.txt'])
        arg_parser.add_argument('-repetitions', nargs=1, type=int, default=[1])
        arg_parser.add_argument('-k', nargs=1, type=int, default=[5])
        arg_parser.add_argument('-l', nargs=1, type=float, default=[5e-3])

        try:
            args = arg_parser.parse_args()
        except:
            self.usage()

        if args.help:
            self.usage()

        return args.file_name[0], args.repetitions[0], args.k[0]


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    main = Main()