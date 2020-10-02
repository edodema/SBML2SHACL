'''
   File name = ttl2sbml.py
   Author = Edoardo De Matteis
   Date created = 8 August 2020
   Python version = 3.8
'''

import re
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-f', '--file', required=True, dest='input_file', metavar='file', help='ttl input file')
parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output', help='sbml output file')
parser.add_argument('-e', '--extended', action='store_true', dest='extended', help='specifies if the model uses Extended SBML')

args = parser.parse_args()

# File IO 
output_file = open(args.output_file, 'w')

# XML tree

class Node:
    '''
    Node represents a node in the Turtle file containting data useful for the SBML translation.

    Attributes 
    ----------
    id: string
    Node's id 'ex:id' as is seen in the Turtle file 

    tag: string 
    Class name that will be used as the XML tag

    attr: dict
    Dictionary containing the pairs <attribute nama, value>

    children: list
    Unsorted children list

    Methods
    -------
    __init__
    set_tag: string -> void
    add_attribute: (string, string) -> void
    add_child: Node -> void
    get_id: () -> string
    get_tag: () -> string
    get_attrib: () -> {string: string}
    get_children: () -> [Node]
    print: () -> ()
    '''

    def __init__(self, id):
        '''
        Instantiate a Node object with the aforementioned attributes. 

        Parameters
        ----------
        id: string
        The id associated to the node

        Return
        -------
        self: Node
        '''
        self.id = id
        self.tag = ''
        self.attrib = {}
        self.children = []

    def set_tag(self, tag):
        '''
        Add a tag to the node

        Parameters
        ----------
        tag: string

        Returns void
        '''
        self.tag = tag

    def add_attribute(self, key, value):
        '''
        Add a {key, value} attribute to the attributes' dictionary

        Parameters
        ----------
        key: string
        value: string

        Returns void
        '''
        self.attrib[key] = value

    def add_child(self, child):
        '''
        Add a child to a node

        Parameters
        ----------
        child: Node

        Returns void
        '''
        self.children.append(child)
    
    def get_id(self):
        '''
        Get a node's id

        Parameters void

        Return
        ------
        id: string
        '''
        return self.id
       
    def get_tag(self):
        '''
        Get a node's tag

         Parameters void

        Return
        ------
        tag: string
        '''
        return self.tag

    def get_attrib(self):
        '''
        Get a node's attribute dictionary

        Parameters void

        Return
        ------
        attrib: {string: string}
        '''
        return self.attrib

    def get_children(self):
        '''
        Get a node's children list
        
        Parameters void

        Return
        ------
        children: [Node]
        '''
        return self.children
        
    def print(self):
        '''
        Prints Node in a human readable way
        
        Parameters void
        
        Returns void
        '''
        print('Object: ', self.id)
        print('Tag: ', self.tag)
        print('Attributes: ', self.attrib)
        print('Children: ', [ child.id for child in self.children ])
        print('')

class Tree:
    ''' 
    Represents a Tree as a root and its Node children

    Attributes
    ----------
    root: Node
    Tree's root

    nodes: [Node]
    A list of nodes 

    Methods
    -------
    __init__
    add_node: Node -> ()
    get_root: () -> Node
    get_nodes: () -> [Node]
    find_node: string -> Node
    print: () -> () 
    '''

    def __init__(self, root):
        '''
        Creates Tree, children are automatically took from the root.

        Parameters
        ---------
        root: Node

        Returns
        -------
        tree: Tree
        '''
        self.root = root
        self.nodes = root.children

    def add_node(self, node):
        '''
        Add a node to nodes' list
        
        Parameters
        ----------
        node: Node
        
        Returns void
        '''
        self.nodes.append(node)

    def get_root(self):
        '''
        Get tree's root
        
        Parameters void

        Return
        ------
        root: Node
        '''
        return self.root
   
    def get_nodes(self):
        '''
        Get tree's nodes

        Parameters void
        
        Return
        ------
        nodes: [Node]
        '''
        return self.nodes
    
    def find_node(self, id):
        '''
        Given a node's id returns the first node with that id

        N.B. The id is unique only based on the correct execution of SHACL2SBML/project/parser/extended_parser.py

        Parameters
        ----------
        id: string

        Return
        ------
        node: Node
        '''
        if self.root.id == id: return self.root 
        for node in self.nodes:
            ret = Tree(node).find_node(id)
            if ret is not None: return ret

    def print(self):
        ''' 
        Prints the tree in a pretty human readable way
        
        Parameters void 
        
        Returns void 
        '''
        self.print_recursive(0) 


    def print_recursive(self, indent):
        ''' 
        self.print() subroutine

        Parameters
        ----------
        indent: number
        An integer used for nodes' indentatio

        Returns void
        '''
        print(' ' * indent, 'Object: ', self.root.id)
        print(' ' * indent, 'Tag: ', self.root.tag)
        print(' ' * indent, 'Attributes: ', self.root.attrib)
        print(' ' * indent, 'Children: ', [ child.id for child in self.root.children ])
        print()

        for node in self.nodes: 
            Tree(node).print_recursive(indent + 4)

# Variables 
root = Node('xml')
'''
xml is the root node since
1. Is in the XML file
2. Node sbml can be found through find_node()
'''
root.set_tag('?xml')
root.add_attribute('version', '"1.0"')
root.add_attribute('encoding', '"UTF-8"')

root.add_child(Node('sbml_1'))

# Extended SBML needs an additional namespace
# comp:required is added since it appears in all MANUAL_*.xml files but is not necessary to test success
if args.extended:
    root.children[0].add_attribute('xmlns:comp', '"http://www.sbml.org/sbml/level3/version1/comp/version1"')
    root.children[0].add_attribute('comp:required', '"true"')

tree = Tree(root) 

# Match strings
extended_tags = '^listOfSubmodels$|^submodel$|^listOfModelDefinitions$|^modelDefinition$|^listOfReplacedElements$|^replacedElement$|^listOfExternalModelDefinitions$|^externalModelDefinition$|^replacedBy$|^listOfDeletions$|^deletion$|^listOfPorts$|^port$'
'''
In extended SBML tags need a 'comp:' header
'''

extended_attributes = '^comp:submodel$|^comp:replacedElement$|^comp:externalModelDefinition$|^comp:replacedBy$|^comp:deletion$|^comp:port$'
'''
Some tags in extended SBML also need the 'comp:' header before their attributes
'''

# Create XML tree, will be later used for parsing
with open(args.input_file) as fp :
    for i, line in enumerate(fp):
        if i > 181 and not line.isspace() :
            if re.match('^ex', line): 
                # Split lines obtaining a triple <s> <p> <o>
                # <o> could have whitespaces so substrings from the third onward are collapsed into one 
                words = line.split()
                del words[-1]
                words[2] = ' '.join(words[2::]) 
                del words[3::]

                # <s>
                subj = re.search('.*:(.*)', words[0]).group(1)
                
                # <p>
                # The predicate can be "a"
                pred = re.search('.*:(.*)', words[1])
                pred = pred.group(1) if pred is not None else 'a'
                
                # Search the node in the tree
                if ( node := tree.find_node(subj)):
                    # Typing
                    if re.match('^a$', pred): 
                        tag = re.search('^schema:(.*)', words[2]).group(1)
                        tag = tag[0].lower() + tag[1:] 

                        # Extended SBML needs a comp: prefix
                        if re.match(extended_tags, tag): tag = 'comp:' + tag
                        node.set_tag(tag)

                    # Add child when object's prefix is ex:
                    elif re.match('^ex:.*' , words[2]):
                        obj = re.search('.*:(.*)', words[2]).group(1)
                        node.add_child(Node(obj))

                    # Add attribute
                    else: 
                        # Attributes can be of two forms
                        # 1. "value"^^xsd:bse_type
                        # 2.  class_type:id
                        # objects can have : in their id so is used non-greedy *? rather than *
                        obj = re.search('(.*)\^\^.*', words[2])
                        obj = obj.group(1) if obj is not None else re.search('.*?:(.*)', words[2]).group(1)

                        # Output value needs to have double quotes "", some attributes could already have them,
                        # is easier to remove them a priori and add them later 
                        obj = obj.strip('"')

                        # Unsupported characters' subsitution
                        obj = re.sub('&', '&amp;', obj)
                        obj = re.sub("'", '&apos;', obj)
                        obj = re.sub('"', '&quot;', obj)

                        # In extended SBML some attributes need the comp: prefix
                        if re.match(extended_attributes, node.tag): pred = 'comp:' + pred

                        node.add_attribute(pred, '"' + obj + '"')

# Convert XML tree to XML text

# Variables 
text = ''
'''
output string
'''

oneliner_tags = '^comp:submodel$|^compartment$|^species$|^parameter$|^unit$|^comp:port$|^comp:deletion$|^comp:replacedElement$|^comp:replacedBy$' 
'''
Tag of labels that have to be written on one line
'''

def xml_parse(tree, indent):
    '''
    Given a tree explores it and writes the XML file - with indentation for readability. 

    Parameters
    ---------
    tree: Tree 
    indent: number

    Returns void
    '''
    global text
    global oneliner_tags

    root = tree.root

    # xml tag behaves differently from others
    if root.id == 'xml': 
        text += '<' + root.tag  
        for key, value in root.attrib.items():
            text += ' ' + key + '=' + value
        text += '?>'
    # Other tags behave the same way
    else: 
        text += '\n' + ' ' * indent + '<' + root.tag 
        for key, value in root.attrib.items():
            text += ' ' + key + '=' + value
        # Oneliners check
        if re.match(oneliner_tags, root.tag): 
            text += '/>'
        else: text += '>'

    # Explore tree
    for child in root.children:
        xml_parse(Tree(child), indent + 2)
    if root.id != 'xml' and not re.match(oneliner_tags, root.tag): text += '\n' + ' ' * indent + '</' + root.tag + '>'
        
# Function call 
xml_parse(tree, 0)

# Output 
output_file.write(text)
output_file.close()
