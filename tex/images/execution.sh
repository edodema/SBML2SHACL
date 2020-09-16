python ./project/parser/extended_parser.py -f ./examples/input/example.xml -o ./examples/output/output.ttl
python ./project/model/shacl_verifier.py -s ./project/model/shapes.ttl -d ./examples/output/output.ttl
True
Validation Report
Conforms: True

python ./project/query/ttl2sbml.py -f ./examples/output/output.ttl -o ./examples/output/output.xml
python ./project/query/query.py -f ./examples/output/output.ttl
http://example.org/ns#compartment_9 a schema:Compartment
http://example.org/ns#compartment_8 a schema:Compartment