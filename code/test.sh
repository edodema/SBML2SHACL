#!/bin/bash
files=(
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000087.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000105.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000399.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000474.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000476.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000559.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000562.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000619.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000624.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000705.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/BIOMD0000000706.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1012110001.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1012220002.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1012220003.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1012220004.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1112260002.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1812100001.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL1904090001.xml"
    "/Users/edodema/Desktop/Projects/SBML2SHACL/input/biomodels/MODEL3632127506.xml"
)

for i in "${files[@]}" 
do
    python parser.py -f $i -o ./output.ttl
    python shacl_verify.py -s ./shapes.ttl -d ./output.ttl
    echo
done
