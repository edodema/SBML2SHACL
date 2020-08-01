import rdflib.graph as G
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-f', '--file', required=True, dest='input_file', metavar='file', help='model file')
parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output', help='output file')

args = parser.parse_args()

# FIle IO
output = open(args.output_file, 'w')

# Query 
graph = G.Graph()
graph.parse(args.input_file, format='ttl')
output.write(graph.serialize(format='pretty-xml').decode('utf-8'))
