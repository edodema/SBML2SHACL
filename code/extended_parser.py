'''
   File name = parser.py
   Author = Edoardo De Matteis
   Date created =  31 July 2020
   Date last modified = 5 August 2020
   Python version = 3.8
'''

import xml.etree.ElementTree as ET 
import argparse
import re

# Command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output')
parser.add_argument('-f', '--file', action='append', required=True, dest='files', metavar='file', help='one or more SBML files')

args = parser.parse_args()

# File IO
output_file = open(args.output_file, 'w')

# Writing preamble necessary for validation
preamble = """
@prefix ex: <http://example.org/ns#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix id: <http://example.org/ns/id#> .
@prefix idref: <http://example.org/ns/idref#> .
@prefix sid: <http://example.org/ns/sid#> .
@prefix sidref: <http://example.org/ns/sid/sidref#> .
@prefix usid: <http://example.org/ns/sid/usid#> .
@prefix usidref: <http://example.org/ns/sid/usid/usidref#> .
@prefix lsid: <http://example.org/ns/sid/lsid#> .
@prefix portsid: <http://example.org/ns/portsid#> .
@prefix portsidref: <http://example.org/ns/portsidref#> .
@prefix sboterm: <http://example.org/ns/sboterm#> .

schema:IDREF rdfs:subClassOf schema:ID . 
schema:SIdRef rdfs:subClassOf schema:SId . 
schema:UnitSId rdfs:subClassOf schema:SId . 
schema:UnitSIdRef rdfs:subClassOf schema:UnitSId . 
schema:PortSId rdfs:subClassOf schema:SId . 
schema:PortSIdRef rdfs:subClassOf schema:PortSId .
schema:LocalSId rdfs:subClassOf schema:SId . 
schema:SBaseRef rdfs:subClassOf schema:SBase .
schema:Sbml rdfs:subClassOf schema:SBase .
schema:ListOfExternalModelDefinitions rdfs:subClassOf schema:SBase .
schema:ExternalModelDefinition rdfs:subClassOf schema:SBase .
schema:Model rdfs:subClassOf schema:SBase .
schema:ListOfUnitDefinitions rdfs:subClassOf schema:SBase .
schema:UnitDefinitions rdfs:subClassOf schema:SBase .
schema:ListOfUnits rdfs:subClassOf schema:SBase .
schema:Unit rdfs:subClassOf schema:SBase .
schema:ListOfCompartments rdfs:subClassOf schema:SBase .
schema:Compartment rdfs:subClassOf schema:SBase .
schema:ListOfSpecies rdfs:subClassOf schema:SBase .
schema:Species rdfs:subClassOf schema:SBase .
schema:ListOfParameters rdfs:subClassOf schema:SBase .
schema:Parameters rdfs:subClassOf schema:SBase .
schema:ListOfSubmodels rdfs:subClassOf schema:SBase .
schema:Submodel rdfs:subClassOf schema:SBase .
schema:ListOfPorts rdfs:subClassOf schema:SBase .
schema:Port rdfs:subClassOf schema:SBaseRef .
schema:ListOfDeletions rdfs:subClassOf schema:SBase .
schema:Deletion rdfs:subClassOf schema:SBaseRef .
schema:ListOfReplacedElements rdfs:subClassOf schema:SBase .
schema:ReplacedElement rdfs:subClassOf schema:SBaseRef .
schema:ReplacedBy rdfs:subClassOf schema:SBaseRef .

usid:ampere a schema:UnitSId .
usid:ampere schema:value "ampere" .
usid:avogadro a schema:UnitSId .
usid:avogadro schema:value "avogadro" . 
usid:becquerel a schema:UnitSId .
usid:becquerel schema:value "becquerel" . 
usid:candela a schema:UnitSId .
usid:candela schema:value "candela" . 
usid:coulomb a schema:UnitSId .
usid:coulomb schema:value "coulomb" .
usid:dimensionless a schema:UnitSId .
usid:dimensionless schema:value "dimensionless" .
usid:farad a schema:UnitSId .
usid:farad schema:value "farad" . 
usid:gram a schema:UnitSId .
usid:gram schema:value "gram" . 
usid:gray a schema:UnitSId .
usid:gray schema:value "gray" . 
usid:henry a schema:UnitSId .
usid:henry schema:value "henry" . 
usid:farad a schema:UnitSId .
usid:farad schema:value "farad" . 
usid:hertz a schema:UnitSId .
usid:hertz schema:value "hertz" . 
usid:item a schema:UnitSId .
usid:item schema:value "item" . 
usid:joule a schema:UnitSId .
usid:joule schema:value "joule" . 
usid:kelvin a schema:UnitSId .
usid:kelvin schema:value "kelvin" . 
usid:kilogram a schema:UnitSId .
usid:kilogram schema:value "kilogram" . 
usid:litre a schema:UnitSId .
usid:litre schema:value "litre" . 
usid:lumen a schema:UnitSId .
usid:lumen schema:value "lumen" . 
usid:lux a schema:UnitSId .
usid:lux schema:value "lux" . 
usid:metre a schema:UnitSId .
usid:metre schema:value "metre" . 
usid:mole a schema:UnitSId .
usid:mole schema:value "mole" . 
usid:newton a schema:UnitSId .
usid:newton schema:value "newton" . 
usid:ohm a schema:UnitSId .
usid:ohm schema:value "ohm" .
usid:pascal a schema:UnitSId .
usid:pascal schema:value "pascal" .
usid:radian a schema:UnitSId .
usid:radian schema:value "radian" .
usid:second a schema:UnitSId .
usid:second schema:value "second" .
usid:siemens a schema:UnitSId .
usid:siemens schema:value "siemens" .
usid:sievert a schema:UnitSId .
usid:sievert schema:value "sievert" .
usid:steradian a schema:UnitSId .
usid:steradian schema:value "steradian" .
usid:tesla a schema:UnitSId .
usid:tesla schema:value "tesla" .
usid:volt a schema:UnitSId .
usid:volt schema:value "volt" .
usid:watt a schema:UnitSId .
usid:watt schema:value "watt" .
usid:weber a schema:UnitSId .
usid:weber schema:value "weber" .

usidref:ampere a schema:UnitSIdRef .
usidref:ampere schema:value "ampere" .
usidref:avogadro a schema:UnitSIdRef .
usidref:avogadro schema:value "avogadro" . 
usidref:becquerel a schema:UnitSIdRef .
usidref:becquerel schema:value "becquerel" . 
usidref:candela a schema:UnitSIdRef .
usidref:candela schema:value "candela" . 
usidref:coulomb a schema:UnitSIdRef .
usidref:coulomb schema:value "coulomb" .
usidref:dimensionless a schema:UnitSIdRef .
usidref:dimensionless schema:value "dimensionless" .
usidref:farad a schema:UnitSIdRef .
usidref:farad schema:value "farad" . 
usidref:gram a schema:UnitSIdRef .
usidref:gram schema:value "gram" . 
usidref:gray a schema:UnitSIdRef .
usidref:gray schema:value "gray" . 
usidref:henry a schema:UnitSIdRef .
usidref:henry schema:value "henry" . 
usidref:farad a schema:UnitSIdRef .
usidref:farad schema:value "farad" . 
usidref:hertz a schema:UnitSIdRef .
usidref:hertz schema:value "hertz" . 
usidref:item a schema:UnitSIdRef .
usidref:item schema:value "item" . 
usidref:joule a schema:UnitSIdRef .
usidref:joule schema:value "joule" . 
usidref:kelvin a schema:UnitSIdRef .
usidref:kelvin schema:value "kelvin" . 
usidref:kilogram a schema:UnitSIdRef .
usidref:kilogram schema:value "kilogram" . 
usidref:litre a schema:UnitSIdRef .
usidref:litre schema:value "litre" . 
usidref:lumen a schema:UnitSIdRef .
usidref:lumen schema:value "lumen" . 
usidref:lux a schema:UnitSIdRef .
usidref:lux schema:value "lux" . 
usidref:metre a schema:UnitSIdRef .
usidref:metre schema:value "metre" . 
usidref:mole a schema:UnitSIdRef .
usidref:mole schema:value "mole" . 
usidref:newton a schema:UnitSIdRef .
usidref:newton schema:value "newton" . 
usidref:ohm a schema:UnitSIdRef .
usidref:ohm schema:value "ohm" .
usidref:pascal a schema:UnitSIdRef .
usidref:pascal schema:value "pascal" .
usidref:radian a schema:UnitSIdRef .
usidref:radian schema:value "radian" .
usidref:second a schema:UnitSIdRef .
usidref:second schema:value "second" .
usidref:siemens a schema:UnitSIdRef .
usidref:siemens schema:value "siemens" .
usidref:sievert a schema:UnitSIdRef .
usidref:sievert schema:value "sievert" .
usidref:steradian a schema:UnitSIdRef .
usidref:steradian schema:value "steradian" .
usidref:tesla a schema:UnitSIdRef .
usidref:tesla schema:value "tesla" .
usidref:volt a schema:UnitSIdRef .
usidref:volt schema:value "volt" .
usidref:watt a schema:UnitSIdRef .
usidref:watt schema:value "watt" .
usidref:weber a schema:UnitSIdRef .
usidref:weber schema:value "weber" .
"""
output_file.write(preamble)

# Subject identifier
subject_id = 0

# Strings for type nodes
id_text = '\n'
idref_text = '\n'
sid_text = '\n'
sidref_text = '\n'
usid_text = '\n'
usidref_text = '\n'
portsid_text = '\n'
portsidref_text = '\n'
sboterm_text = '\n'

# Lists mantaining type nodes to avoid
# multiple instantiation 
id_list = []
idref_list = []
sid_list = []
sidref_list = []
usid_list = ['ampere', 'avogadro', 'becquerel', 'candela', 'coulomb', 'dimensionless',
                 'farad', 'gram', 'gray', 'henry', 'hertz', 'item', 'joule', 'kelvin', 'kilogram',
                 'litre', 'lumen', 'lux', 'metre', 'mole', 'newton', 'ohm', 'pascal', 'radian', 
                 'second', 'siemens', 'sievert', 'steradian', 'tesla', 'volt', 'watt', 'weber']
usidref_list = usid_list.copy()
portsid_list = []
portsidref_list = []
sboterm_list = []

# String for nodes instances
text = '\n'

# Check for compound types attributes 
def add_identifier(idt, value, idt_list):
    """
    Instantiate a node of a type defined in the SHACL model 
    and it to a check list.

    Parameters
    ----------
    idt : string  
        Type's prefix.
    value : string
        Node's only attribute's value.
    idt_list: list
        The check list where the node will be added.

    Returns
    -------
    text : string
        SHACL statements for the creation of the node. 

    >>> add_identifier('id', 'secret', sid_list)
    id:secret a schema:ID .
    id:secret schema:value "secret"^^xsd:string .
    """
    identifiers = {
        'id': 'ID', 'idref': 'IDREF',
        'sid': 'SId', 'sidref': 'SIdRef',
        'usid': 'UnitSId', 'usidref': 'UnitSIdRef',
        'portsid': 'PortSId', 'portsidref': 'PortSIdRef',
        'sboterm': 'SBOTerm'
    }
    '''
    Dictionary associating each prefix to its type.
    '''

    if not idt in identifiers: 
        print("ERROR! This identifier is not modeled.")
        exit(-1)
    
    text = '\n' + idt + ':' + value + ' a schema:' + identifiers[idt]  + ' .'
    text += '\n' + idt + ':' + value + ' schema:value "' + value + '"^^xsd:string .'
    idt_list.append(value)
    return text

# XML exploration
# Search function  
def xml_search(root, father):
    """
    Converts a given SBML model in SHACL exploring the 
    XML file as a tree

    Parameters
    ----------
    root: Element
    The radix of the subtree to explore

    father: string
    Root parent's tag 

    subject_id: integer 
    Counter of the given construct, added to the root's 
    tag defines the identifier

    Returns void
    """
    
    # Necessary to be global since Python does not  have call by reference
    global id_text
    global idref_text
    global sid_text
    global sidref_text
    global usid_text
    global usidref_text
    global portsid_text
    global portsidref_text
    global sboterm_text
    global subject_id
    global text

    # Increment id counter
    subject_id += 1

    # Isolate tag name
    tag = re.search('.*\}(.*)', root.tag)
    tag = tag.group(1) if tag is not None else root.tag

    # This match guarantees that we will check only defined constructs,
    # remove the whole conditional to blindly convert all constructs, even
    # though it is no problem for the parser shapes.ttl should be updated
    if not re.match('^sbml$|^listOfExternalModelDefinitions$|^externalModelDefinition$|^listOfModelDefinitions$|^modelDefinition$|^model$|^listOfUnitDefinitions$|^unitDefinition$|^listOfUnits$|^unit$|^listOfCompartments$|^compartment$|^listOfSpecies$|^species$|^listOfParameter$|^parameter$|^listOfSubmodels$|^submodel$|^listOfPorts$|^port$|^listOfDeletions$|^deletion$|^listOfReplacedElements$|^replacedElement$|^replacedBy$', tag): return

    subject = tag + '_' + str(subject_id)
    '''
    Defines the subject identifier 
    '''

    # xmlns in sbml is not treated as an attribute since is a namespace
    if(tag == 'sbml'): 
        text += 'ex:%s schema:xmlns "%s"^^xsd:anyURI .\n' % (subject, re.search('{(.*)}.*', root.tag).group(1))

    # Resolve relation attributes fot parent node
    if father: text += 'ex:%s schema:%s ex:%s .\n' % (father, tag, subject)
    
    # Type definition
    text += 'ex:%s a schema:%s .\n' % (subject, tag[0].upper() + tag[1:])
    
    # Attributes
    for ext_key, value in root.attrib.items():
        
        # Isolate attribute name
        key = re.search('.*\}(.*)', ext_key)
        key = key.group(1) if key is not None else ext_key 

        # Attributes' typing
        if re.match('^id$', key):
            # id has different types depending on the tag used 
            if tag == 'unitDefinition':
                text += 'ex:%s schema:%s usid:%s .\n' % (subject, key, value)
                # id is a UnitSId: ussid:value schema:value value
                if not value in usid_list: usid_text += add_identifier('usid', value, usid_list) 
            elif tag == 'port':
                text += 'ex:%s schema:%s portsid:%s .\n' % (subject, key, value)
                # id is a PortSId: sid:value schema:value value
                if not value in portsid_list: portsid_text += add_identifier('portsid', value, portsid_list)
            else:
                text += 'ex:%s schema:%s sid:%s .\n' % (subject, key, value)
                # id is a SId: sid:value schema:value value
                if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)

        elif re.match('^name$', key):
            text += 'ex:%s schema:%s "%s"^^xsd:string .\n' % (subject, key, value)

        elif re.match('^metaid$', key):
            text += 'ex:%s schema:%s id:%s .\n' % (subject, key, value)
            # id is a ID: id:value schema:value value
            if not value in id_list: id_text += add_identifier('id', value, id_list)

        elif re.match('^sboTerm$', key):
            text += 'ex:%s schema:%s sboterm:%s .\n' % (subject, key, value)
            # id is a SBOTerm: sboterm:value schema:value value
            if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)

        elif re.match('^substanceUnits$|^timeUnits$|^volumeUnits$|^areaUnits$|^lengthUnits$|^extentUnits$|^units$|^unitRef$', key):
            text += 'ex:%s schema:%s usidref:%s .\n' % (subject, key, value)
            # id is a UnitSIdRef: usidref:value schema:value value
            if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)

        elif re.match('^conversionFactor$|^compartment$|^timeConversionFactor$|^extentConversionFactor$|^idRef$|^modelRef$|^submodelRef$|^deletion$', key):
            text += 'ex:%s schema:%s sidref:%s .\n' % (subject, key, value)
            # id is a SIdRef: usidref:value schema:value value
            if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)

        elif re.match('^kind$', key):
            text += 'ex:%s schema:%s usid:%s .\n' % (subject, key, value)
            # id is a UnitSId: usid:value schema:value value
            if not value in usid_list: usid_text += add_identifier('usid', value, usid_list)

        elif re.match('^exponent$|^multiplier$|^spatialDimensions$|^size$|^initialAmount$|^initialConcentration$|^value$', key):
            text += 'ex:%s schema:%s "%s"^^xsd:decimal .\n' % (subject, key, value)

        elif re.match('^scale$|^level$|^version$', key):
            text += 'ex:%s schema:%s "%s"^^xsd:integer .\n' % (subject, key, value)

        elif re.match('^constant$|^hasOnlySubstanceUnits$|^boundaryCondition$', key):
            text += 'ex:%s schema:%s "%s"^^xsd:boolean .\n' % (subject, key, value)

        elif re.match('^source', key):
            text += 'ex:%s schema:%s "%s"^^xsd:anyURI .\n' % (subject, key, value)
        
        elif re.match('^portRef$', key):
            text += 'ex:%s schema:%s portsidref:%s .\n' % (subject, key, value)
            # portRef is a PortSIdRef: portsidref:value schema:value value
            if not value in portsidref_list: portsidref_text += add_identifier('portsidref', value, portsidref_list)

        elif re.match('^metaIdRef$', key):
            text += 'ex:%s schema:%s idref:%s .\n' % (subject, key, value)
            # metaIdRef is a IDREF: idref:value schema:value value
            if not value in idref_list: idref_text += add_identifier('idref', value, idref_list)
 
    text += '\n'
    for child in root: 
        xml_search(child, subject)

for model in args.files:
    '''
    This loop allows to have multiple files in input.
    '''
    tree = ET.ElementTree(file=model)
    root = tree.getroot()
    xml_search(root, '')

output_file.write(id_text)
output_file.write(idref_text)
output_file.write(sid_text)
output_file.write(sidref_text)
output_file.write(usid_text)
output_file.write(usidref_text)
output_file.write(portsid_text)
output_file.write(portsidref_text)
output_file.write(sboterm_text)

output_file.write(text)

output_file.close()