import xml.etree.ElementTree as ET
import re 

preamble = "./code/preamble.txt"

#model = "./input/biomodels/BIOMD0000000562.xml"
#model = "./input/biomodels/BIOMD0000000476.xml"
#model = "./input/biomodels/MODEL1112260002.xml"
model = "./input/biomodels/MODEL1904090001.xml"
output = "./code/output.ttl"

# Writing preamble 
output_file = open(output, 'w')
output_file.write(open(preamble, 'r').read())

# XML parsing 
tree = ET.parse(model)
root = tree.getroot()

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

# XML tree exploration
for child in root.iter():
    tag = re.search('.*\}(.*)', child.tag)
    if tag is not None: tag = tag.group(1)

    #if re.match('BaseRef', tag) is not None: print(child.tag, child.attrib)

    if re.match('sbml', tag) is not None: 
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
            if re.match('id', key) is not None: 
                sbml_text += subject + ' schema:id sid:' + value + ' .'
                # id is a SId: sid:value schema:value value
                if not value in sid_list:
                    sid_text += '\nsid:' + value + ' a schema:SId .'
                    sid_text += '\nsid:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sid_list.append(value)
            # Ssbml> <name> <value>
            elif re.match('name', key) is not None: 
                sbml_text += subject + ' schema:name "' + value + '"^^xsd:string .'  
            # <Sbml> <metaid> <value>
            elif re.match('metaid', key) is not None:
                sbml_text += subject + ' schema:metaid id:' + value + ' .'
                # metid is a ID: id:value schema:value value  
                if not value in id_list:
                    id_text += '\nid:' + value + ' a schema:ID .'
                    id_text += '\nid:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    id_list.append(value)
            # <Sbml> <sboTerm> <value>
            elif re.match('sboTerm', key) is not None: 
                sbml_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                # sboTerm is a SBOTerm: sboterm:value schema:value value
                if not value in sboterm_list:
                    sboterm_text += '\nsboterm:' + value + ' a schema:SBOTerm .'
                    sboterm_text += '\nsboterm:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sboterm_list.append(value)
            # <Sbml> <level> <value>
            elif re.match('level', key) is not None: 
                sbml_text += subject + ' schema:level "' + value + '"^^xsd:integer .'
            # <Sbml> <version> <value>
            elif re.match('version', key) is not None: 
                sbml_text += subject + ' schema:version "' + value + '"^^xsd:integer .'
        # Increment Sbml identifier
        sbml_count += 1

    '''
    elif re.match('listOfExternalModelDefinition', tag) is not None: print(child.tag, child.attrib)
    elif re.match('externalModelDefinition', tag) is not None: print(child.tag, child.attrib)
    elif re.match('listOfModelDefinitions', tag) is not None: print(child.tag, child.attrib)
    '''

    if re.match('model', tag) is not None:
        # a Model has associated a Sbml whose attribute is now added
        # hence model is used as an object despite the subject variable
        # <Sbml> <model> <Model>
        subject = 'ex:model_' + str(model_count)  
        sbml_text += '\nex:sbml_' + str(sbml_count-1) + ' schema:model ' + subject + ' .'
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
            if re.match('id', key) is not None: 
                model_text += subject + ' schema:id sid:' + value + ' .'
                # id is a SId: sid:value schema:value value
                if not value in sid_list:
                    sid_text += '\nsid:' + value + ' a schema:SId .'
                    sid_text += '\nsid:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sid_list.append(value)
            # <Model> <name> <value>
            elif re.match('name', key) is not None: 
                model_text += subject + ' schema:name "' + value + '"^^xsd:string .' 
            # <Model> <metaid> <value>
            elif re.match('metaid', key) is not None:
                model_text += subject + ' schema:metaid id:' + value + ' .'
                # metaid is a ID: id:value schema:value value
                if not value in id_list:
                    id_text += '\nid:' + value + ' a schema:ID .'
                    id_text += '\nid:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    id_list.append(value)
            # <Model> <sboTerm> <value>
            elif re.match('sboTerm', key) is not None: 
                model_text += subject + ' schema:sboTerm sboterm:' + value + ' .'
                # sboTerm is a SBOTerm: sboterm:value schema:value value
                if not value in sboterm_list:
                    sboterm_text += '\nsboterm:' + value + ' a schema:SBOTerm .'
                    sboterm_text += '\nsboterm:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sboterm_list.append(value)
            # <Model> <substanceUnits> <value>
            elif re.match('substanceUnits', key) is not None:
                model_text += subject + ' schema:substanceUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <timeUnits> <value>
            elif re.match('timeUnits', key) is not None:
                model_text += subject + ' schema:timeUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <volumeUnits> <value>
            elif re.match('volumeUnits', key) is not None:
                model_text += subject + ' schema:volumeUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <areaUnits> <value>
            elif re.match('areaUnits', key) is not None:
                model_text += subject + ' schema:areaUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <lengthUnits> <value>
            elif re.match('lengthUnits', key) is not None:
                model_text += subject + ' schema:lengthUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <extentUnits> <value>
            elif re.match('extentUnits', key) is not None:
                model_text += subject + ' schema:extentUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <conversionFactor> <value>
            elif re.match('conversionFactor', key) is not None:
                model_text += subject + ' schema:conversionFactor usidref:' + value + ' .'
                # is a SIdRef: sidref:value schema:value value
                if not value in sidref_list:
                    sidref_text += '\nsidref:' + value + ' a schema:SIdRef .'
                    sidref_text += '\nsidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sidref_list.append(value)
            # Increment Model identifier
            model_count += 1

    '''
    elif re.match('listOfUnitDefinition', tag) is not None: print(tag, child.attrib)
    elif re.match('unitDefinitions', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfUnits', tag) is not None: print(tag, child.attrib)
    elif re.match('unit', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfCompartments', tag) is not None: print(tag, child.attrib)
    elif re.match('compartment', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfSpecies', tag) is not None: print(tag, child.attrib)
    elif re.match('species', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfParameters', tag) is not None: print(tag, child.attrib)
    elif re.match('parameter', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfSubmodels', tag) is not None: print(tag, child.attrib)
    elif re.match('submodel', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfPorts', tag) is not None: print(tag, child.attrib)
    elif re.match('port', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfDeletions', tag) is not None: print(tag, child.attrib)
    elif re.match('deletion', tag) is not None: print(tag, child.attrib)
    elif re.match('listOfReplacedElements', tag) is not None: print(tag, child.attrib)
    elif re.match('replacedElement', tag) is not None: print(tag, child.attrib)
    elif re.match('replacedBy', tag) is not None: print(tag, child.attrib)
    '''

# Writing on file

output_file.write(id_text)
output_file.write(sid_text)
output_file.write(sidref_text)
output_file.write(usid_text)
output_file.write(usidref_text)
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