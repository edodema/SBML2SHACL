import rdflib
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-f', '--file', required=True, dest='input_file', metavar='file', help='model file')
#parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output', help='output file')

args = parser.parse_args()

# Query 

g = rdflib.Graph()

g.parse(args.input_file, format='ttl')
result = g.query("""
PREFIX schema: <http://schema.org/>

CONSTRUCT {
        ?p schema:has ?o
}
WHERE {
    ex:model_1 ?p ?o
}
""")

for row in result:
    print("%s %s %s" % row)