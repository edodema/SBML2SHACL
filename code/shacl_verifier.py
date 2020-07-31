import argparse
from pyshacl import validate

# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-s', '--shapes', required=True, dest='shapes_file', metavar='shapes', help='shapes file')
parser.add_argument('-d', '--data', required=True, dest='data_file', metavar='data', help='data file')

args = parser.parse_args()

# Validation 
conforms, v_graph, v_text = validate(args.data_file, shacl_graph=args.shapes_file,
   inference='rdfs', debug=True, serialize_report_graph=True)

print(conforms)
#print(v_graph)
print(v_text)