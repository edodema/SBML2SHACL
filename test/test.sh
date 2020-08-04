#!/bin/bash
files=(
    "input/biomodels/BIOMD0000000087.xml"
    "input/biomodels/BIOMD0000000105.xml"
    "input/biomodels/BIOMD0000000399.xml"
    "input/biomodels/BIOMD0000000474.xml"
    "input/biomodels/BIOMD0000000476.xml"
    "input/biomodels/BIOMD0000000559.xml"
    "input/biomodels/BIOMD0000000562.xml"
    "input/biomodels/BIOMD0000000619.xml"
    "input/biomodels/BIOMD0000000624.xml"
    "input/biomodels/BIOMD0000000705.xml"
    "input/biomodels/BIOMD0000000706.xml"
    "input/biomodels/MODEL1012110001.xml"
    "input/biomodels/MODEL1012220002.xml"
    "input/biomodels/MODEL1012220003.xml"
    "input/biomodels/MODEL1012220004.xml"
    "input/biomodels/MODEL1112260002.xml"
    "input/biomodels/MODEL1812100001.xml"
    "input/biomodels/MODEL1904090001.xml"
    "input/biomodels/MODEL3632127506.xml"
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
        #python ../code/parser.py -f ./$i -f $j -o ./output/output.ttl
        python ../code/extended_parser.py -f ./$i -f $j -o ./output/output.ttl
        python ../code/shacl_verifier.py -s ../code/shapes.ttl -d ./output/output.ttl
    done
done
