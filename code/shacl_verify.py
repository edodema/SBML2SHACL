import sys
from pyshacl import validate
from os import path

shapes_file = "./code/shapes.ttl"
data_file = "./code/data.ttl"

conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
   inference='rdfs', debug=True, serialize_report_graph=True)

#print(conforms)
#print(v_graph)
print(v_text)

######## command line version, use this in the final version
#if len(sys.argv) != 3: 
#    print('help: insert shape file as first argument and data file as the second one.')
#    exit(1)

#shapes_file = sys.argv[1]
#data_file = sys.argv[2]

#conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
#   inference='rdfs', debug=True, serialize_report_graph=True)

#print(conforms)
#print(v_graph)
#print(v_text)