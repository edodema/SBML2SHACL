'''
   File name = query.py
   Author = Edoardo De Matteis
   Date created = 1 August 2020
   Python version = 3.8
'''

import rdflib
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-f', '--file', required=True, dest='input_file', metavar='file', help='model file')

args = parser.parse_args()

# Query 
g = rdflib.Graph()

g.parse(args.input_file, format='ttl')

result = g.query("""
PREFIX schema: <http://schema.org/>

SELECT ?s
WHERE {
    ?s a schema:Compartment
}
""")

for row in result:
    print("%s a schema:Compartment" % row)