#!/bin/bash
#########################################
#   File name = test.sh
#   Author = Edoardo De Matteis
#   Date created = 31 July 2020
#########################################

# Uncomment input/Custom/* to execute tests on hierarchical SBML
# keep in mind that they work only with extended_parser.py
files=(
    "input/biomodel/BIOMD0000000087.xml"
    "input/biomodel/BIOMD0000000105.xml"
    "input/biomodel/BIOMD0000000399.xml"
    "input/biomodel/BIOMD0000000474.xml"
    "input/biomodel/BIOMD0000000476.xml"
    "input/biomodel/BIOMD0000000559.xml"
    "input/biomodel/BIOMD0000000562.xml"
    "input/biomodel/BIOMD0000000619.xml"
    "input/biomodel/BIOMD0000000624.xml"
    "input/biomodel/BIOMD0000000705.xml"
    "input/biomodel/BIOMD0000000706.xml"
    "input/biomodel/MODEL1012110001.xml"
    "input/biomodel/MODEL1012220002.xml"
    "input/biomodel/MODEL1012220003.xml"
    "input/biomodel/MODEL1012220004.xml"
    "input/biomodel/MODEL1112260002.xml"
    "input/biomodel/MODEL1812100001.xml"
    "input/biomodel/MODEL3632127506.xml"
    #"input/Custom/MANUAL_1.xml"
    #"input/Custom/MANUAL_2.xml"
    #"input/Custom/MANUAL_3.xml"
    #"input/Custom/MANUAL_4.xml"
)

for i in "${files[@]}" 
do
    for j in "${files[@]}"
    do
        echo $i
        echo $j
        #python ../project/parser/parser.py -f ./$i -f $j -o ./output/output.ttl
        python ../project/parser/extended_parser.py -f ./$i -f ./$j -o ./output/output.ttl
        python ../project/model/shacl_verifier.py -s ../project/model/shapes.ttl -d ./output/output.ttl
    done
done
