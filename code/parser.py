import xml.etree.ElementTree as ET
import re 

model = "./code/MODEL0568648427.xml"
output = "./code/output.ttl"

# Writing preamble 
output_file = open(output, 'w')
output_file.write(
    """@prefix ex: <http://example.org/ns#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix id: <http://example.org/ns/id#> .
@prefix sid: <http://example.org/ns/sid#> .
@prefix sidref: <http://example.org/ns/sid/sidref#> .
@prefix usid: <http://example.org/ns/sid/usid#> .
@prefix usidref: <http://example.org/ns/sid/usid/usidref#> .
@prefix lsid: <http://example.org/ns/sid/lsid#> .
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
usid:weber schema:value "weber" ."""
)

# XML parsing 
tree = ET.parse(model)
root = tree.getroot()

# XML tree exploration
for child in root.iter():
    if re.match(".*sBaseRef$", child.tag): print(child.tag, child.attrib)
    if re.match(".*sbml$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfExternalModelDefinition*$", child.tag): print(child.tag, child.attrib)
    if re.match(".*model$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfUnitModelDefinition$", child.tag): print(child.tag, child.attrib)
    if re.match(".*unitDefinitions$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfUnits$", child.tag): print(child.tag, child.attrib)
    if re.match(".*unit$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfCompartments$", child.tag): print(child.tag, child.attrib)
    if re.match(".*compartment$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfSpecies$", child.tag): print(child.tag, child.attrib)
    if re.match(".*species$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfParameters$", child.tag): print(child.tag, child.attrib)
    if re.match(".*parameter$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfSubmodels$", child.tag): print(child.tag, child.attrib)
    if re.match(".*submodel$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfPorts$", child.tag): print(child.tag, child.attrib)
    if re.match(".*port$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfDeletions$", child.tag): print(child.tag, child.attrib)
    if re.match(".*deletion$", child.tag): print(child.tag, child.attrib)
    if re.match(".*listOfReplacedElements$", child.tag): print(child.tag, child.attrib)
    if re.match(".*replacedElement$", child.tag): print(child.tag, child.attrib)
    if re.match(".*replacedBy$", child.tag): print(child.tag, child.attrib)

output_file.close()