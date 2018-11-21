import sys
import getopt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, help='Symbol')
parser.add_argument('input', type=str, help="Input file")
args = parser.parse_args()

print(args)