# SBML2SHACL
SBML2SHACL is a repository that allows you to convert a SBML file in a SHACL graph, it does not support all SBML's constructs but only a subset composed by Extended SBML and the following constructs typical of classic SBML:
* Parameter
* Compartment  
* Unit 
* Species 

For further considerations see the [diagram](diagram/diagram.png) or the [documentation](#resources).


## Code 
Here is a brief description of what programs in the [code](code) directory do, notice that python programs depend on the [rdflib](https://github.com/RDFLib/rdflib) library. The input SBML file is a priori assumed to be correct so please [verify](http://sbml.org/Facilities/Validator) it beforehand.
### Shapes
[shapes.ttl](code/shapes.ttl) defines a Turtle model of SBML constructs and types as ontologies, some prefixes are dummies (i.e. ex and type ones). 
### Parser
There are two different parsers. The [first one](code/parser.py) does not support extended SBML since it iterates through the XML file like a list rather than a tree and keeping track of submodels is complex. The [second parser](code/extended_parser.py) can be more easily extended since it relies more on the input file's correctness assumption, it also supports extended SBML and the code is shorter and faster. 

| File | CPU usage | System time (s) | User time (s) | Total |
| - | - | - | - | - |
| parser.py | 97 % | 52.90 | 2445.38 | 42:54.54 |
| extended_parser.py | 97 % | 42.48 | 833.54 | 15:02.19 |

### Shacl verifier
To check the correctness of the parser's output file use [shacl_verifier.py](code/shacl_verifier.py).
### Query 
To execute queries on the parser's output file use [query.py](code/query.py), unlike other files that one does not take command line arguments since the print specification changes dependently by the query hence you have to hardcode it.
### Turtle to XML 
A query represents the same knowledge as a XML file and each Turtle triple
```
_:subject _:predicate _:object .
```
can be converted to XML as 
```
<subject>
    <predicate> object </predicate>
</subject>
```
Using [ttl2xml.py](code/ttl2xml.py) is possible to convert a whole Turtle file in XML, keep in mind that XML does not necessarily mean SBML.

# Test
In the [eponymous](test/test.sh) directory can be found:
* 19 [SBML models](test/input/biomodel) downloaded from [Biomodels](https://www.ebi.ac.uk/biomodels/) for classic SBML
* 4 [SBML models](test/input/custom) for extended SBML. 
* [test.sh](test/test.sh) that uses the aforementioned tests to check the parsers correctness. 

## Resources 
* [The Systems Biology Markup Language (SBML): Language Specification for Level 3 Version 2 Core](http://co.mbine.org/specifications/sbml.level-3.version-2.core.release-2.pdf)
* [SBML Level 3 Package Specification Hierarchical Model Composition](https://authors.library.caltech.edu/50975/1/sbml-comp-version-1-release-3.pdf)
* [Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/)
