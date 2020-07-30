import xml.etree.ElementTree as ET
import re 

# Function that istantiates an identifier in the output file
def add_identifier(idt, value, idt_list):
    identifiers = {
        'id': 'ID', 'idref': 'IDREF',
        'sid': 'SId', 'sidref': 'SIdRef',
        'usid': 'UnitSId', 'usidref': 'UnitSIdRef',
        'sboterm': 'SBOTerm'
    }

    if not idt in identifiers: 
        print("ERROR! This identifier is not modeled.")
        exit(-1)

    text = '\n' + idt + ':' + value + ' a schema:' + identifiers[idt]  + ' .'
    text += '\n' + idt + ':' + value + ' schema:value "' + value + '"^^xsd:string .'
    idt_list.append(value)
    return text

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
    tag = tag.group(1) if tag is not None else child.tag

    #if re.match('BaseRef', tag) is not None: print(child.tag, child.attrib)

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
            # Ssbml> <name> <value>
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

    # elif re.match('listOfExternalModelDefinition', tag) is not None: print(child.tag, child.attrib)
    # elif re.match('externalModelDefinition', tag) is not None: print(child.tag, child.attrib)
    # elif re.match('listOfModelDefinitions', tag) is not None: print(child.tag, child.attrib)

    elif re.match('^model$', tag) is not None:
        # a Model is associated to a Sbml whose attribute is now added
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
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <timeUnits> <value>
            elif re.match('^timeUnits$', key) is not None:
                model_text += subject + ' schema:timeUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <volumeUnits> <value>
            elif re.match('^volumeUnits$', key) is not None:
                model_text += subject + ' schema:volumeUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <areaUnits> <value>
            elif re.match('^areaUnits$', key) is not None:
                model_text += subject + ' schema:areaUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <lengthUnits> <value>
            elif re.match('^lengthUnits$', key) is not None:
                model_text += subject + ' schema:lengthUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <extentUnits> <value>
            elif re.match('^extentUnits$', key) is not None:
                model_text += subject + ' schema:extentUnits usidref:' + value + ' .'
                # is a UnitSIdRef: usidref:value schema:value value
                if not value in usidref_list:
                    usidref_text += '\nusidref:' + value + ' a schema:UnitSIdRef .'
                    usidref_text += '\nusidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    usidref_list.append(value)
            # <Model> <conversionFactor> <value>
            elif re.match('^conversionFactor$', key) is not None:
                model_text += subject + ' schema:conversionFactor usidref:' + value + ' .'
                # is a SIdRef: sidref:value schema:value value
                if not value in sidref_list:
                    sidref_text += '\nsidref:' + value + ' a schema:SIdRef .'
                    sidref_text += '\nsidref:' + value + ' schema:value "' + value + '"^^xsd:string .'
                    sidref_list.append(value)
        # Increment Model identifier
        model_count += 1

    elif re.match('^listOfUnitDefinitions$', tag) is not None: 
        # a ListOfUnitDefinitions is associated to a Model whose attribute is now added
        # hence listOfUnitDefinitions is used as an object despite the subject variable
        # <Model> <listOfUnitDefinitions> <ListOfUnitDefinitions>
        subject = 'ex:listOfUnitDefinitions'  
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

    elif re.match('^unitDefinition$', tag) is not None:
        # a UnitDefinition is associated to a ListOfUnitDefinitions whose attribute is now added
        # hence unitDefinition is used as an object despite the subject variable
        # <ListOfUnitDefinitions> <unitDefinition> <UnitDefinition>
        subject = 'ex:unitDefinition_' + str(unitDefinition_count)  
        listOfUnitDefinitions_text += '\nex:listOfUnitDefinitions schema:unitDefinition ' + subject + ' .'
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
                if not value in sid_list: usid_text += add_identifier('usid', value, usid_list)
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
        listOfUnits_text += '\nex:listOfUnits schema:unit ' + subject + ' .'
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
                sbml_text += subject + ' schema:multiplier "' + value + '"^^xsd:decimal .'
            # <Unit> <scale> <value>
            elif re.match('^scale$', key) is not None: 
                sbml_text += subject + ' schema:scale "' + value + '"^^xsd:integer .'
            # <Unit> <exponent> <value>
            elif re.match('^exponent$', key) is not None: 
                sbml_text += subject + ' schema:exponent "' + value + '"^^xsd:decimal .'
        # Increment Unit identifier
        unit_count += 1

    
    '''
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