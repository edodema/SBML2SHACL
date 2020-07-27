from pyshacl import validate
from os import path

shapes_file = "./code/shapes.ttl"
data_file = "./code/data.ttl"

conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file, 
    inference='rdfs', debug=True, serialize_report_graph=True)

#print(conforms)
#print(v_graph)
print(v_text)