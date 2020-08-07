'''
   File name = ttl2sbml.py
   Author = Edoardo De Matteis
   Date created = 6 August 2020
   Date last modified = 
   Python version = 3.8
'''

import re
import argparse


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
    set_tag: 
    add_attribute
    add_child
    get_id
    get_tag
    get_attrib
    get_children
    '''

    def __init__(self, id):
        '''
        Instantiate a Node object with the aforementioned attributes. 
        '''
        self.id = id
        self.tag = ''
        self.attrib = {}
        self.children = []

    def set_tag(self, tag):
        '''
        Add a tag to the node
        '''
        self.tag = tag

    def add_attribute(self, key, value):
        '''
        Add a key and a value to the attributes' dictionary
        '''
        self.attrib[key] = value

    def add_child(self, child):
        '''
        Add a child to a node
        '''
        self.children.append(child)
    
    def get_id(self):
        '''
        Returns id
        '''
        return self.id
       
    def get_tag(self):
        '''
        Returns tag
        '''
        return self.tag

    def get_attrib(self):
        '''
        Returns attributes
        '''
        return self.attrib

    def get_children(self):
        '''
        Returns children
        '''
        return self.children
        
    def print(self):
        '''
        Prints in a pretty way a Node's attributes
        '''
        print('Object: ', self.id)
        print('Tag: ', self.tag)
        print('Attributes: ', self.attrib)
        print('Children: ', [ child.id for child in self.children ])
        print('')

class Tree:
    ''' 
    Represents a collection of Nodes

    Attributes
    ----------
    root: Node
    Tree's root

    nodes: list
    A list of nodes 

    Methods
    -------
    __init__
    set_root
    add_node
    get_root
    find_node
    print
    '''

    def __init__(self, root):
        '''
        Create Tree object, the children list is copied since Python assigns object by reference.
        To be fair I do not think it should be a problem but since there is only one Tree 
        memory usage is negligible. I think is desiderable that children and nodeas are shared. 
        Let's see if I have to change it
        '''
        self.root = root
        #self.nodes = root.children.copy()
        self.nodes = root.children

    def set_root(self, root):
        '''
        Sets root for a tree
        '''
        self.root = root

    def add_node(self, node):
        '''
        Add node to nodes list
        '''
        self.nodes.append(node)

    def get_root(self):
        '''
        Returns root
        '''
        return self.root
   
    def get_nodes(self):
        '''
        Returns nodes
        '''
        return self.nodes
    
    def find_node(self, id):
        '''
        If present returns a node for a given id
        '''
        if self.root.id == id: return self.root 
        for node in self.nodes:
            ret = Tree(node).find_node(id)
            if ret is not None: return ret

    def print(self):
        ''' 
        Prints tree in a pretty way
        '''
        self.print_recursive(0) 


    def print_recursive(self, indent):
        ''' 
        Suberoutine to print tree in a pretty way
        '''
        print(' ' * indent, 'Object: ', self.root.id)
        print(' ' * indent, 'Tag: ', self.root.tag)
        print(' ' * indent, 'Attributes: ', self.root.attrib)
        print(' ' * indent, 'Children: ', [ child.id for child in self.root.children ])
        print()

        for node in self.nodes: 
            Tree(node).print_recursive(indent + 8)



# Command line arguments
parser = argparse.ArgumentParser()
   
parser.add_argument('-f', '--file', required=True, dest='input_file', metavar='file', help='ttl input file')
parser.add_argument('-o', '--output', required=True, dest='output_file', metavar='output', help='sbml output file')

args = parser.parse_args()

# File IO 
output_file = open(args.output_file, 'w') 

# Writing is done using two strings 
head_text = '\n'
'''
This one will open xml labels
'''

tail_text = '\n'
'''
This one will close xml labels
'''

# Nodes construction
root = Node('xml')
root.set_tag('?xml')
root.add_attribute('version', '"1.0"')
root.add_attribute('encoding', '"UTF-8"')
'''
I consider xml as the root node since
1. Exists
2. sbml can be find through find_node()
'''
root.add_child(Node('sbml_0'))
tree = Tree(root)

with open(args.input_file) as fp :
    for i, line in enumerate(fp):
        if i > 181 and not line.isspace() :
            if re.match('^ex', line): 
                # Separate lines by whitespaces obtaining a triple <s> <p> <o>
                words = line.split()

                subj = re.search('.*:(.*)', words[0]).group(1)

                # The predicate can be "a"
                pred = re.search('.*:(.*)', words[1])
                pred = pred.group(1) if pred is not None else 'a'
                
                # The object is a primitive type "A"^^xsd:B or a URI ex:C
                obj = re.search('(.*)\^\^.*', words[2])
                obj = obj.group(1) if obj is not None else re.search('.*:(.*)', words[2]).group(1)

                # Search the node in the tree
                if ( node := tree.find_node(subj)):
                    # Typing
                    if re.match('a', pred):  node.set_tag(obj)
                    # Add child
                    elif re.match('^sbml$|^listOfExternalModelDefinitions$|^externalModelDefinition$|^listOfModelDefinitions$|^modelDefinition$|^model$|^listOfUnitDefinitions$|^unitDefinition$|^listOfUnits$|^unti$|^listOfCompartments$|^compartment$|^listOfSpecies$|^species$|^listOfParameter$|^parameter$|^listOfSubmodels$|^submodel$|^listOfPorts$|^port$|^listOfDeletions$|^deletions$|^listOfReplacedElements$|^replacedElement$|^replacedBy$', pred): 
                        node.add_child(Node(obj))
                    # Add attribute
                    else: node.add_attribute(pred, obj)
                
                # This should never occur since I add nodes one after another
                else:
                    #pass
                    print(subj, pred, obj)


                output_file.write(subj + ' ' + pred + ' ' + obj + '\n')                

print()
tree.print()

#print(tree.find_node('submodel_1'))

output_file.close()