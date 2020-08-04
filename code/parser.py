import argparse
import xml.etree.ElementTree as ET
import re 
from os import path

# Function that istantiates an identifier in the output file
def add_identifier(idt, value, idt_list):
    identifiers = {
        'id': 'ID', 'idref': 'IDREF',
        'sid': 'SId', 'sidref': 'SIdRef',
        'usid': 'UnitSId', 'usidref': 'UnitSIdRef',
        'portsid': 'PortSId', 'portsidref': 'PortSIdRef',
        'sboterm': 'SBOTerm'
    }

    if not idt in identifiers: 
        print("ERROR! This identifier is not modeled.")
        exit(-1)

    text = '\n' + idt + ':' + value + ' a schema:' + identifiers[idt]  + ' .'
    text += '\n' + idt + ':' + value + ' schema:value "' + value + '"^^xsd:string .'
    idt_list.append(value)
    return text

# Command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output')
parser.add_argument('-f', '--file', action='append', required=True, dest='files', metavar='file', help='one or more SBML files')

args = parser.parse_args()

# File definitions
output = args.output_file
input_files = args.files

# Writing preamble 

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

output_file = open(output, 'w')

output_file.write(preamble)

# Flags
model_flag = True

# Counters
sBaseRef_count = 1
sbml_count = 1
listOfExternalModelDefinitions_count = 1
externalModelDefinition_count = 1
listOfModelDefinitions_count = 1
model_count = 1
listOfUnitDefinitions_count = 1
unitDefinition_count = 1
listOfUnits_count = 1
unit_count = 1
listOfCompartments_count = 1
compartment_count = 1
listOfSpecies_count = 1
species_count = 1
listOfParameters_count = 1
parameter_count = 1
listOfSubmodels_count = 1
submodel_count = 1
listOfPorts_count = 1
port_count = 1
listOfDeletions_count = 1
deletion_count = 1
listOfReplacedElements_count =1
replacedElement_count = 1
replacedBy_count = 1

# Strings mantaining text to write 
id_text = '\n'
idref_text = '\n'
sid_text = '\n'
sidref_text = '\n'
usid_text = '\n'
usidref_text = '\n'
portsid_text = '\n'
portsidref_text = '\n'
sboterm_text = '\n'

sBaseRef_text = '\n'
sbml_text = '\n'
listOfExternalModelDefinitions_text = '\n'
externalModelDefinition_text = '\n'
listOfModelDefinitions_text = '\n'
model_text = '\n'
listOfUnitDefinitions_text = '\n'
unitDefinition_text = '\n'
listOfUnits_text = '\n'
unit_text = '\n'
listOfCompartments_text = '\n'
compartment_text = '\n'
listOfSpecies_text = '\n'
species_text = '\n'
listOfParameters_text = '\n'
parameter_text = '\n'
listOfSubmodels_text = '\n'
submodel_text = '\n'
listOfPorts_text = '\n'
port_text = '\n'
listOfDeletions_text = '\n'
deletion_text = '\n'
listOfReplacedElements_text ='\n'
replacedElement_text = '\n'
replacedBy_text = '\n'

# lists, useful for not writing more than once the same identifier
# for readability and efficiency
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

# XML parsing 

for model in input_files: 
    tree = ET.parse(model)
    root = tree.getroot()

    # XML tree exploration
    for child in root.iter():
        tag = re.search('.*\}(.*)', child.tag)
        tag = tag.group(1) if tag is not None else child.tag

        #if re.match('^SBaseRef', tag) is not None: pass

        if re.match('^sbml$', tag) is not None: 
            # Subject parametrization, is simply useful 
            subject = '\nex:sbml_' + str(sbml_count) 
            sbml_text += subject + ' a schema:Sbml .'
            # xmlns attribute, ET treats it differently
            sbml_text += (subject + ' schema:xmlns "' +
                re.search('^\{(.*)\}', child.tag).group(1) 
                + '"^^xsd:anyURI .') 
            # Attributes 
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Sbml> <key> <value> 

                # <Sbml> <id> <value>
                if re.match('^id$', key) is not None: 
                    sbml_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Sbml> <name> <value>
                elif re.match('^name$', key) is not None: 
                    sbml_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Sbml> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    sbml_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Sbml> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    sbml_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Sbml> <level> <value>
                elif re.match('^level$', key) is not None: 
                    sbml_text += subject + ' schema:level "' + value + '"^^xsd:integer .'
                # <Sbml> <version> <value>
                elif re.match('^version$', key) is not None: 
                    sbml_text += subject + ' schema:version "' + value + '"^^xsd:integer .'
            # Increment Sbml identifier
            sbml_count += 1

        elif re.match('listOfExternalModelDefinition$', tag) is not None:
            # a ListOfExternalModelDefinition is associated to a Sbml whose attribute is now added
            # hence listOfExternalModelDefinition is used as an object despite the subject variable
            # <Sbml> <listOfExternalModelDefinition> <ListOfExternalModelDefinition>
            subject = 'ex:listOfExternalModelDefinition_' + str(listOfUnitDefinitions_count) 
            sbml_text += '\nex:sbml_' + str(sbml_count-1) + ' schema:listOfExternalModelDefinition ' + subject + ' .'
            subject = '\n' + subject 
            listOfExternalModelDefinitions_text += subject + ' a schema:ListOfExternalModelDefinition .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfExternalModelDefinition> <key> <value> 

                # <ListOfExternalModelDefinition> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfExternalModelDefinitions_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfExternalModelDefinition> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfExternalModelDefinitions_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfExternalModelDefinition> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfExternalModelDefinitions_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfExternalModelDefinition> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfExternalModelDefinitions_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # Increment ListOfExternalModelDefinition identifier
            listOfExternalModelDefinitions_count += 1

        elif re.match('externalModelDefinition$', tag) is not None:
            # a ExternalModelDefinition is associated to a ListOfExternalModelDefinition whose attribute is now added
            # hence externalModelDefinition is used as an object despite the subject variable
            # <ListOfExternalModelDefinition> <externalModelDefinition> <ExternalModelDefinition>
            subject = 'ex:externalModelDefinition_' + str(externalModelDefinition_count) 
            listOfExternalModelDefinitions_text += '\nex:listOfExternalModelDefinition_' + str(listOfExternalModelDefinitions_count-1) + ' schema:externalModelDefinition ' + subject + ' .'
            subject = '\n' + subject         
            externalModelDefinition_text += subject + ' a schema:externalModelDefinition .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ExternalModelDefinition> <key> <value> 
    
                # <ExternalModelDefinition> <id> <value> 
                if re.match('^id$', key) is not None: 
                    externalModelDefinition_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ExternalModelDefinition> <name> <value>
                elif re.match('^name$', key) is not None: 
                    externalModelDefinition_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <ExternalModelDefinition> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    externalModelDefinition_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ExternalModelDefinition> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    externalModelDefinition_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <ExternalModelDefinition> <source> <value>
                elif re.match('^source$', key):
                    externalModelDefinition_text += subject + ' schema:source "' + value + '"^^xsd:anyURI .'
                # <ExternalModelDefinition> <modelRef> <value>
                elif re.match('^modelRef$', key):
                    externalModelDefinition_text += subject + ' schema:modelRef "' + value + '"^^xsd:decimal .'  
                    # modelRef is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ExternalModelDefinition> <md5> <value>
                elif re.match('^md5$', key):
                    externalModelDefinition_text += subject + ' schema:md5 "' + value + '"^^xsd:string .'  
            # Increment Unit identifier
            externalModelDefinition_count += 1

        elif re.match('listOfModelDefinition$', tag) is not None:
            # a ListOfModelDefinition is associated to a Sbml whose attribute is now added
            # hence listOfModelDefinition is used as an object despite the subject variable
            # <Sbml> <listOfModelDefinition> <ListOfModelDefinition>
            subject = 'ex:listOfModelDefinition_' + str(listOfUnitDefinitions_count) 
            sbml_text += '\nex:sbml_' + str(sbml_count-1) + ' schema:listOfModelDefinition ' + subject + ' .'
            subject = '\n' + subject 
            listOfModelDefinitions_text += subject + ' a schema:ListOfModelDefinition .'
            model_flag = False
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfModelDefinition> <key> <value> 

                # <ListOfModelDefinition> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfModelDefinitions_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfModelDefinition> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfModelDefinitions_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfModelDefinition> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfModelDefinitions_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfModelDefinition> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfModelDefinitions_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # Increment ListOfModelDefinition identifier
            listOfModelDefinitions_count += 1

        elif re.match('^model$', tag) is not None:
            # a Model is associated to a Sbml whose attribute is now added
            # hence model is used as an object despite the subject variable
            # <Sbml> <model> <Model>
            subject = 'ex:model_' + str(model_count) 
            if model_flag: 
                sbml_text += '\nex:sbml_' + str(sbml_count-1) + ' schema:model ' + subject + ' .'
            else:
                sbml_text += '\nex:listOfModelDefinition_' + str(listOfModelDefinitions_count-1) + ' schema:model ' + subject + ' .'
            subject = '\n' + subject
            # from here we will use model only as a subject
            model_text += subject + ' a schema:Model .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Model> <key> <value> 

                # <Model> <id> <value>
                if re.match('^id$', key) is not None: 
                    model_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Model> <name> <value>
                elif re.match('^name$', key) is not None: 
                    model_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <Model> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    model_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Model> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    model_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Model> <substanceUnits> <value>
                elif re.match('^substanceUnits$', key) is not None:
                    model_text += subject + ' schema:substanceUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <timeUnits> <value>
                elif re.match('^timeUnits$', key) is not None:
                    model_text += subject + ' schema:timeUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <volumeUnits> <value>
                elif re.match('^volumeUnits$', key) is not None:
                    model_text += subject + ' schema:volumeUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <areaUnits> <value>
                elif re.match('^areaUnits$', key) is not None:
                    model_text += subject + ' schema:areaUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <lengthUnits> <value>
                elif re.match('^lengthUnits$', key) is not None:
                    model_text += subject + ' schema:lengthUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <extentUnits> <value>
                elif re.match('^extentUnits$', key) is not None:
                    model_text += subject + ' schema:extentUnits usidref:' + value + ' .'
                    # is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Model> <conversionFactor> <value>
                elif re.match('^conversionFactor$', key) is not None:
                    model_text += subject + ' schema:conversionFactor usidref:' + value + ' .'
                    # is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
            # Increment Model identifier
            model_count += 1

        elif re.match('^listOfUnitDefinitions$', tag) is not None: 
            # a ListOfUnitDefinitions is associated to a Model whose attribute is now added
            # hence listOfUnitDefinitions is used as an object despite the subject variable
            # <Model> <listOfUnitDefinitions> <ListOfUnitDefinitions>
            subject = 'ex:listOfUnitDefinitions_' + str(listOfUnitDefinitions_count) 
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfUnitDefinitions ' + subject + ' .'
            subject = '\n' + subject 
            listOfUnitDefinitions_text += subject + ' a schema:ListOfUnitDefinitions .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfUnitDefinitions> <key> <value> 

                # <ListOfUnitDefinitions> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfUnitDefinitions_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfUnitDefinitions> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfUnitDefinitions_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfUnitDefinitions_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfUnitDefinitions_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # Increment ListOfUnitDefinitions identifier
            listOfUnitDefinitions_count += 1

        elif re.match('^unitDefinition$', tag) is not None:
            # a UnitDefinition is associated to a ListOfUnitDefinitions whose attribute is now added
            # hence unitDefinition is used as an object despite the subject variable
            # <ListOfUnitDefinitions> <unitDefinition> <UnitDefinition>
            subject = 'ex:unitDefinition_' + str(unitDefinition_count)  
            listOfUnitDefinitions_text += ('\nex:listOfUnitDefinitions_' + str(listOfUnitDefinitions_count-1) + 
                ' schema:listOfUnitDefinitions ' + subject + ' .')
            subject = '\n' + subject         
            unitDefinition_text += subject + ' a schema:UnitDefinition .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key

                ## <UnitDefinition> <key> <value> 
                # <UnitDefinition> <name> <value>
                if re.match('^name$', key) is not None: 
                    unitDefinition_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <UnitDefinition> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    unitDefinition_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <UnitDefinition> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    unitDefinition_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <UnitDefinition> <id> <value>
                if re.match('^id$', key) is not None: 
                    unitDefinition_text += subject + ' schema:id usid:' + value + ' .'
                    # id is a UnitSId: usid:value schema:value value
                    if not value in usid_list: usid_text += add_identifier('usid', value, usid_list)
            # Increment UnitDefinition identifier
            unitDefinition_count += 1
            
        elif re.match('^listOfUnits$', tag) is not None:
            # a ListOfUnits is associated to a UnitDefinition whose attribute is now added
            # hence listOfUnits is used as an object despite the subject variable
            # <UnitDefinition> <listOfUnits> <ListOfUnits>
            subject = 'ex:listOfUnits_' + str(listOfUnits_count)
            unitDefinition_text += '\nex:unitDefinition_' + str(unitDefinition_count-1) + ' schema:listOfUnits ' + subject + ' .'
            subject = '\n' + subject 
            listOfUnits_text += subject + ' a schema:ListOfUnits .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfUnits> <key> <value> 
    
                # <ListOfUnitDefinitions> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfUnits_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfUnits> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfUnits_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnits> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfUnits_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnits> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfUnits_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # Increment ListOfUnits identifier
            listOfUnits_count += 1
    
        elif re.match('^unit$', tag) is not None:
            # a Unit is associated to a ListOfUnits whose attribute is now added
            # hence unit is used as an object despite the subject variable
            # <ListOfUnits> <unit> <Unit>
            subject = 'ex:unit_' + str(unit_count)  
            listOfUnits_text += '\nex:listOfUnits_' + str(listOfUnits_count-1) + ' schema:unit ' + subject + ' .'
            subject = '\n' + subject         
            unit_text += subject + ' a schema:Unit .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Unit> <key> <value> 
    
                # <Unit> <id> <value> 
                if re.match('^id$', key) is not None: 
                    unit_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Unit> <name> <value>
                elif re.match('^name$', key) is not None: 
                    unit_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Unit> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    unit_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Unit> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    unit_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Unit> <kind> <value>
                if re.match('^kind$', key) is not None: 
                    unit_text += subject + ' schema:kind usid:' + value + ' .'
                    # kind is a UnitSId: usid:value schema:value value
                    if not value in usid_list: usid_text += add_identifier('usid', value, usid_list)
                # <Unit> <multiplier> <value>
                elif re.match('^multiplier$', key) is not None: 
                    unit_text += subject + ' schema:multiplier "' + value + '"^^xsd:decimal .'
                # <Unit> <scale> <value>
                elif re.match('^scale$', key) is not None: 
                    unit_text += subject + ' schema:scale "' + value + '"^^xsd:integer .'
                # <Unit> <exponent> <value>
                elif re.match('^exponent$', key) is not None: 
                    unit_text += subject + ' schema:exponent "' + value + '"^^xsd:decimal .'
            # Increment Unit identifier
            unit_count += 1
    
        elif re.match('^listOfCompartments$', tag) is not None:
            # a ListOfCompartments is associated to a Model whose attribute is now added
            # hence listOfCompartments is used as an object despite the subject variable
            # <Model> <listOfCompartments> <ListOfCompartments>
            subject = 'ex:listOfCompartments_' + str(listOfCompartments_count) 
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfCompartments ' + subject + ' .'
            subject = '\n' + subject 
            listOfCompartments_text += subject + ' a schema:ListOfCompartments .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfCompartments> <key> <value> 
    
                # <ListOfCompartments> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfCompartments_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfCompartments> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfCompartments_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfCompartments_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfCompartments_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfCompartments_count += 1
    
        elif re.match('^compartment$', tag) is not None:
            # a Compartment is associated to a ListOfCompartments whose attribute is now added
            # hence compartment is used as an object despite the subject variable
            # <ListOfCompartments> <compartment> <Compartment>
            subject = 'ex:compartment_' + str(compartment_count) 
            listOfCompartments_text += '\nex:listOfCompartments_' + str(listOfCompartments_count-1) + ' schema:compartment ' + subject + ' .'
            subject = '\n' + subject         
            compartment_text += subject + ' a schema:Compartment .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Compartment> <key> <value> 
    
                # <Compartment> <id> <value> 
                if re.match('^id$', key) is not None: 
                    compartment_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Compartment> <name> <value>
                elif re.match('^name$', key) is not None: 
                    compartment_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Compartment> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    compartment_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Compartment> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    compartment_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Compartment> <spatialDimensions> <value>
                elif re.match('^spatialDimensions$', key):
                    compartment_text += subject + ' schema:spatialDimensions "' + value + '"^^xsd:decimal .'  
                # <Compartment> <size> <value>
                elif re.match('^size$', key):
                    compartment_text += subject + ' schema:size "' + value + '"^^xsd:decimal .'  
                # <Compartment> <constant> <value>
                elif re.match('^constant$', key):
                    compartment_text += subject + ' schema:constant "' + value + '"^^xsd:boolean .'  
                # <Compartment> <units> <value> 
                elif re.match('^units$', key) is not None: 
                    compartment_text += subject + ' schema:units usidref:' + value + ' .'
                    # units is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
            # Increment Unit identifier
            compartment_count += 1
    
        elif re.match('^listOfSpecies$', tag) is not None:
            # a ListOfSpecies is associated to a Model whose attribute is now added
            # hence listOfSpecies is used as an object despite the subject variable
            # <Model> <listOfSpecies> <ListOfSpecies>
            subject = 'ex:listOfSpecies_' + str(listOfSpecies_count)
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfSpecies ' + subject + ' .'
            subject = '\n' + subject 
            listOfSpecies_text += subject + ' a schema:ListOfSpecies .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfSpecies> <key> <value> 
    
                # <ListOfSpecies> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfSpecies_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfSpecies> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfSpecies_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfSpecies_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfSpecies_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfSpecies_count += 1
        
        elif re.match('^species$', tag) is not None:
            # a Species is associated to a ListOfSpecies whose attribute is now added
            # hence species is used as an object despite the subject variable
            # <ListOfSpecies> <species> <Species>
            subject = 'ex:species_' + str(species_count) 
            listOfSpecies_text += '\nex:listOfSpecies_' + str(listOfSpecies_count-1) + ' schema:species ' + subject + ' .'
            subject = '\n' + subject         
            species_text += subject + ' a schema:Species .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Species> <key> <value> 
    
                # <Species> <id> <value> 
                if re.match('^id$', key) is not None: 
                    species_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Species> <name> <value>
                elif re.match('^name$', key) is not None: 
                    species_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Species> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    species_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Species> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    species_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Species> <compartment> <value>
                elif re.match('^compartment$', key):
                    species_text += subject + ' schema:compartment sidref:' + value + ' .'
                    # compartment is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <Species> <initialAmount> <value>
                elif re.match('^size$', key):
                    species_text += subject + ' schema:initialAmount "' + value + '"^^xsd:decimal .'  
                # <Species> <initialConcentration> <value>
                elif re.match('^size$', key):
                    species_text += subject + ' schema:initialConcentration "' + value + '"^^xsd:decimal .'  
                # <Species> <substanceUnits> <value> 
                elif re.match('^substanceUnits$', key) is not None: 
                    species_text += subject + ' schema:substanceUnits usidref:' + value + ' .'
                    # units is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Species> <hasOnlySubstanceUnits> <value>
                elif re.match('^hasOnlySubstanceUnits$', key):
                    species_text += subject + ' schema:hasOnlySubstanceUnits "' + value + '"^^xsd:boolean .'  
                # <Species> <boundaryCondition> <value>
                elif re.match('^boundaryCondition$', key):
                    species_text += subject + ' schema:boundaryCondition "' + value + '"^^xsd:boolean .'  
                # <Species> <constant> <value>
                elif re.match('^constant$', key):
                    species_text += subject + ' schema:constant "' + value + '"^^xsd:boolean .'  
                # <Species> <conversionFactor> <value>
                elif re.match('^conversionFactor$', key):
                    species_text += subject + ' schema:conversionFactor sidref:' + value + ' .'
                    # conversionFactor is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
            # Increment Unit identifier
            species_count += 1
    
        elif re.match('^listOfParameters$', tag) is not None:
             # a ListOfParameters is associated to a Model whose attribute is now added
            # hence listOfParameters is used as an object despite the subject variable
            # <Model> <listOfParameters> <ListOfParameters>
            subject = 'ex:listOfParameters_' + str(listOfParameters_count) 
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfParameters ' + subject + ' .'
            subject = '\n' + subject 
            listOfParameters_text += subject + ' a schema:ListOfParameters .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfParameters> <key> <value> 
    
                # <ListOfParameters> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfParameters_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfParameters> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfParameters_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfParameters_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfParameters_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfParameters_count += 1
    
        elif re.match('^parameter$', tag) is not None: 
            # a Parameter is associated to a ListOfParameters whose attribute is now added
            # hence parameter is used as an object despite the subject variable
            # <ListOfParameters> <parameter> <Parameter>
            subject = 'ex:parameter_' + str(parameter_count) 
            listOfParameters_text += '\nex:listOfParameters_' + str(listOfParameters_count-1) + ' schema:parameter ' + subject + ' .'
            subject = '\n' + subject         
            parameter_text += subject + ' a schema:Parameter .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Parameter> <key> <value> 
    
                # <Parameter> <id> <value> 
                if re.match('^id$', key) is not None: 
                    parameter_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Parameter> <name> <value>
                elif re.match('^name$', key) is not None: 
                    parameter_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Parameter> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    parameter_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <Parameter> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    parameter_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Parameter> <value> <value>
                elif re.match('^value$', key):
                    parameter_text += subject + ' schema:value "' + value + '"^^xsd:decimal .'  
                # <Parameter> <units> <value> 
                elif re.match('^units$', key) is not None: 
                    parameter_text += subject + ' schema:units usidref:' + value + ' .'
                    # units is a UnitSIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Parameter> <constant> <value>
                elif re.match('^constant$', key):
                    parameter_text += subject + ' schema:constant "' + value + '"^^xsd:boolean .'  
            # Increment Unit identifier
            parameter_count += 1
        '''   
        elif re.match('listOfSubmodels$', tag) is not None:
            # a ListOfSubmodels is associated to a Model whose attribute is now added
            # hence listOfSubmodels is used as an object despite the subject variable
            # <Model> <listOfSubmodels> <ListOfSubmodels>
            subject = 'ex:listOfSubmodels_' + str(listOfSubmodels_count)
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfSubmodels ' + subject + ' .'
            subject = '\n' + subject 
            listOfSubmodels_text += subject + ' a schema:ListOfSubmodels .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfSubmodels> <key> <value> 
    
                # <ListOfSubmodels> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfSubmodels_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfSubmodels> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfSubmodels_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfSubmodels_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfSubmodels_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfSubmodels_count += 1
        
        elif re.match('submodel$', tag) is not None:
            # a Submodel is associated to a ListOfSubmodels whose attribute is now added
            # hence submodel is used as an object despite the subject variable
            # <ListOfSubmodels> <submodel> <Submodel>
            subject = 'ex:submodel_' + str(submodel_count) 
            listOfSubmodels_text += '\nex:listOfSubmodels_' + str(listOfSubmodels_count-1) + ' schema:submodel ' + subject + ' .'
            subject = '\n' + subject         
            submodel_text += subject + ' a schema:Submodel .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Submodel> <key> <value> 
    
                # <Submodel> <id> <value> 
                if re.match('^id$', key) is not None: 
                    submodel_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <Submodel> <name> <value>
                elif re.match('^name$', key) is not None: 
                    submodel_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Submodel> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    submodel_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)  
                # <Submodel> <sboTerm> <value> 
                elif re.match('^sboTerm$', key) is not None: 
                    submodel_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Submodel> <modelRef> <value>
                elif re.match('^modelRef$', key):
                    submodel_text += subject + ' schema:modelRef sidref:' + value + ' .'
                    # modelRef is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <Submodel> <timeConversionFactor> <value>
                elif re.match('^timeConversionFactor$', key):
                    submodel_text += subject + ' schema:timeConversionFactor sidref:' + value + ' .'
                    # timeConversionFactor is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <Submodel> <extentConversionFactor> <value>
                elif re.match('^extentConversionFactor$', key):
                    submodel_text += subject + ' schema:extentConversionFactor sidref:' + value + ' .'
                    # extentConversionFactor is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
            # Increment Unit identifier
            submodel_count += 1
        
        elif re.match('listOfPorts$', tag) is not None:
            # a ListOfPorts is associated to a Model whose attribute is now added
            # hence listOfPorts is used as an object despite the subject variable
            # <Model> <listOfPorts> <ListOfPorts>
            subject = 'ex:listOfPorts_' + str(listOfPorts_count)
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfPorts ' + subject + ' .'
            subject = '\n' + subject 
            listOfPorts_text += subject + ' a schema:ListOfPorts .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfPorts> <key> <value> 
    
                # <ListOfPorts> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfPorts_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfPorts> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfPorts_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfPorts_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfPorts_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfPorts_count += 1

        elif re.match('port$', tag) is not None:
            # a Port is associated to a ListOfPorts whose attribute is now added
            # hence port is used as an object despite the subject variable
            # <ListOfPorts> <port> <Port>
            subject = 'ex:port_' + str(port_count) 
            listOfPorts_text += '\nex:listOfPorts_' + str(listOfPorts_count-1) + ' schema:port ' + subject + ' .'
            subject = '\n' + subject         
            port_text += subject + ' a schema:Port .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Port> <key> <value> 
    
                # <Port> <id> <value> 
                if re.match('^id$', key) is not None: 
                    port_text += subject + ' schema:id portsid:' + value + ' .'
                    # id is a PortSId: portsid:value schema:value value
                    if not value in portsid_list: portsid_text += add_identifier('portsid', value, portsid_list)
                # <Port> <name> <value>
                elif re.match('^name$', key) is not None: 
                    port_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Port> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    port_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)  
                # <Port> <sboTerm> <value> 
                elif re.match('^sboTerm$', key) is not None: 
                    port_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # Increment Unit identifier
            port_count += 1

        elif re.match('listOfDeletions$', tag) is not None:
            # a ListOfDeletions is associated to a Subodel whose attribute is now added
            # hence listOfDeletions is used as an object despite the subject variable
            # <Model> <listOfDeletions> <ListOfDeletions>
            subject = 'ex:listOfDeletions_' + str(listOfDeletions_count)
            submodel_text += '\nex:submodel_' + str(submodel_count-1) + ' schema:listOfDeletions ' + subject + ' .'
            subject = '\n' + subject 
            listOfDeletions_text += subject + ' a schema:ListOfDeletions .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfDeletions> <key> <value> 

                # <ListOfDeletions> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfDeletions_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfDeletions> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfDeletions_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfDeletions_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfDeletions_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfDeletions_count += 1
        
        elif re.match('deletion$', tag) is not None:
            # a Deletion is associated to a ListOfDeletions whose attribute is now added
            # hence deletion is used as an object despite the subject variable
            # <ListOfDeletions> <deletion> <Deletion>
            subject = 'ex:deletion_' + str(deletion_count) 
            listOfDeletions_text += '\nex:listOfDeletions_' + str(listOfDeletions_count-1) + ' schema:deletion ' + subject + ' .'
            subject = '\n' + subject         
            deletion_text += subject + ' a schema:Deletion .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <Deletion> <key> <value> 
    
                # <Deletion> <id> <value> 
                if re.match('^id$', key) is not None: 
                    deletion_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_list += add_identifier('sid', value, sid_list)
                # <Deletion> <name> <value>
                elif re.match('^name$', key) is not None: 
                    deletion_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <Deletion> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    deletion_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)  
                # <Deletion> <sboTerm> <value> 
                elif re.match('^sboTerm$', key) is not None: 
                    deletion_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <Deletion> <idRef> <value> 
                elif re.match('^idRef$', key) is not None: 
                    deletion_text += subject + ' schema:idRef idref:' + value + ' .'
                    # idRef is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <Deletion> <portRef> <value> 
                elif re.match('^portRef$', key) is not None: 
                    deletion_text += subject + ' schema:portRef portsidref:' + value + ' .'
                    # portRef is a PortSIdRef: portsidref:value schema:value value
                    if not value in portsidref_list: portsidref_text += add_identifier('portsidref', value, portsidref_list)
                # <Deletion> <unitRef> <value> 
                elif re.match('^unitRef$', key) is not None: 
                    deletion_text += subject + ' schema:unitRef usidref:' + value + ' .'
                    # unitRef is a USIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <Deletion> <metaIdRef> <value> 
                elif re.match('^metaIdRef$', key) is not None: 
                    deletion_text += subject + ' schema:metaIdRef idref:' + value + ' .'
                    # unitRef is a USIdRef: usidref:value schema:value value
                    if not value in idref_list: idref_text += add_identifier('idref', value, idref_list)
            # Increment Unit identifier
            deletion_count += 1
    
        elif re.match('listOfReplacedElements$', tag) is not None:
            # a ListOfReplacedElements is associated to a Model whose attribute is now added
            # hence listOfReplacedElements is used as an object despite the subject variable
            # <Model> <listOfReplacedElements> <ListOfReplacedElements>
            subject = 'ex:listOfReplacedElements_' + str(listOfReplacedElements_count)
            model_text += '\nex:model_' + str(model_count-1) + ' schema:listOfReplacedElements ' + subject + ' .'
            subject = '\n' + subject 
            listOfReplacedElements_text += subject + ' a schema:ListOfReplacedElements .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ListOfReplacedElements> <key> <value> 
    
                # <ListOfReplacedElements> <id> <value>
                if re.match('^id$', key) is not None: 
                    listOfReplacedElements_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ListOfReplacedElements> <name> <value>
                elif re.match('^name$', key) is not None: 
                    listOfReplacedElements_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ListOfUnitDefinitions> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    listOfReplacedElements_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ListOfUnitDefinitions> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    listOfReplacedElements_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
            # increment counter
            listOfReplacedElements_count += 1

        elif re.match('replacedElement$', tag) is not None:
            # a ReplacedElements is associated to a ListOfReplacedElementss whose attribute is now added
            # hence replacedElement is used as an object despite the subject variable
            # <ListOfReplacedElementss> <replacedElement> <ReplacedElements>
            subject = 'ex:replacedElement_' + str(replacedElement_count) 
            listOfReplacedElements_text += '\nex:listOfReplacedElements_' + str(listOfReplacedElements_count-1) + ' schema:replacedElement ' + subject + ' .'
            subject = '\n' + subject         
            replacedElement_text += subject + ' a schema:ReplacedElement .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ReplacedElements> <key> <value> 
    
                # <ReplacedElements> <id> <value> 
                if re.match('^id$', key) is not None: 
                    replacedElement_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_list += add_identifier('sid', value, sid_list)
                # <ReplacedElements> <name> <value>
                elif re.match('^name$', key) is not None: 
                    replacedElement_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
                # <ReplacedElements> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    replacedElement_text += subject + ' schema:metaid id:' + value + ' .'
                    # metid is a ID: id:value schema:value value  
                    if not value in id_list: id_text += add_identifier('id', value, id_list)  
                # <ReplacedElements> <sboTerm> <value> 
                elif re.match('^sboTerm$', key) is not None: 
                    replacedElement_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <ReplacedElements> <idRef> <value> 
                elif re.match('^idRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:idRef idref:' + value + ' .'
                    # idRef is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <ReplacedElements> <portRef> <value> 
                elif re.match('^portRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:portRef portref:' + value + ' .'
                    # portRef is a PortSIdRef: portsidref:value schema:value value
                    if not value in portsidref_list: portsidref_text += add_identifier('portsidref', value, portsidref_list)
                # <ReplacedElements> <unitRef> <value> 
                elif re.match('^unitRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:unitRef usidref:' + value + ' .'
                    # unitRef is a USIdRef: usidref:value schema:value value
                    if not value in usidref_list: usidref_text += add_identifier('usidref', value, usidref_list)
                # <ReplacedElements> <metaIdRef> <value> 
                elif re.match('^metaIdRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:metaIdRef idref:' + value + ' .'
                    # unitRef is a USIdRef: usidref:value schema:value value
                    if not value in idref_list: idref_text += add_identifier('idref', value, idref_list)
                # <ReplacedElements> <submodelRef> <value> 
                elif re.match('^submodelRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:submodelRef idref:' + value + ' .'
                    # submodelRef is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <ReplacedElements> <deletion> <value> 
                elif re.match('^deletion$', key) is not None: 
                    replacedElement_text += subject + ' schema:deletion idref:' + value + ' .'
                    # deletion is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
                # <ReplacedElements> <conversionFactor> <value> 
                elif re.match('^conversionFactor$', key) is not None: 
                    replacedElement_text += subject + ' schema:conversionFactor idref:' + value + ' .'
                    # conversionFactor is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
            # Increment Unit identifier
            replacedElement_count += 1
    
        elif re.match('replacedBy$', tag) is not None:
            # a ReplacedBy is associated to a Model whose attribute is now added
            # hence replacedBy is used as an object despite the subject variable
            # <Model> <replacedBy> <ReplacedBy>
            subject = 'ex:replacedBy_' + str(replacedBy_count) 
            model_text += '\nex:model_' + str(model_count-1) + ' schema:replacedBy ' + subject + ' .'
            subject = '\n' + subject 
            replacedBy_text += subject + ' a schema:ReplacedBy .'
            # Attributes
            for child_key, value in child.attrib.items():
                # Some tags could have a namespace before, remove it 
                key = re.search('.*\}(.*)', child_key)
                key = key.group(1) if key is not None else child_key
                ## <ReplacedBy> <key> <value> 
    
                # <ReplacedBy> <id> <value>
                if re.match('^id$', key) is not None: 
                    replacedBy_text += subject + ' schema:id sid:' + value + ' .'
                    # id is a SId: sid:value schema:value value
                    if not value in sid_list: sid_text += add_identifier('sid', value, sid_list)
                # <ReplacedBy> <name> <value>
                elif re.match('^name$', key) is not None: 
                    replacedBy_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
                # <ReplacedBy> <metaid> <value>
                elif re.match('^metaid$', key) is not None:
                    replacedBy_text += subject + ' schema:metaid id:' + value + ' .'
                    # metaid is a ID: id:value schema:value value
                    if not value in id_list: id_text += add_identifier('id', value, id_list)
                # <ReplacedBy> <sboTerm> <value>
                elif re.match('^sboTerm$', key) is not None: 
                    replacedBy_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                    # sboTerm is a SBOTerm: sboterm:value schema:value value
                    if not value in sboterm_list: sboterm_text += add_identifier('sboterm', value, sboterm_list)
                # <ReplacedBy> <submodelRef> <value> 
                elif re.match('^submodelRef$', key) is not None: 
                    replacedElement_text += subject + ' schema:submodelRef idref:' + value + ' .'
                    # submodelRef is a SIdRef: sidref:value schema:value value
                    if not value in sidref_list: sidref_text += add_identifier('sidref', value, sidref_list)
            # increment counter
            replacedBy_count += 1
        '''
# Writing on file

output_file.write(id_text)
output_file.write(idref_text)
output_file.write(sid_text)
output_file.write(sidref_text)
output_file.write(usid_text)
output_file.write(usidref_text)
output_file.write(portsid_text)
output_file.write(portsidref_text)
output_file.write(sboterm_text)

output_file.write(sBaseRef_text)
output_file.write(sbml_text)
output_file.write(listOfExternalModelDefinitions_text)
output_file.write(externalModelDefinition_text)
output_file.write(listOfModelDefinitions_text)
output_file.write(model_text)
output_file.write(listOfUnitDefinitions_text)
output_file.write(unitDefinition_text)
output_file.write(listOfUnits_text)
output_file.write(unit_text)
output_file.write(listOfCompartments_text)
output_file.write(compartment_text)
output_file.write(listOfSpecies_text)
output_file.write(species_text)
output_file.write(listOfParameters_text)
output_file.write(parameter_text)
output_file.write(listOfSubmodels_text)
output_file.write(submodel_text)
output_file.write(listOfPorts_text)
output_file.write(port_text)
output_file.write(listOfDeletions_text)
output_file.write(deletion_text)
output_file.write(listOfReplacedElements_text)
output_file.write(replacedElement_text)
output_file.write(replacedBy_text)

output_file.close()
