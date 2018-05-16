""" file:   validation.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Handles validation against EarthChem's API schema
"""

from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import requests

import os
import pkg_resources

# We're not live updating at the moment but it's nice to have this recoded somewhere
SOAP_SCHEMA_URL = 'http://ecp.iedadata.org/soap_search_schema.xsd'
SOAP_SCHEMA = pkg_resources.resource_filename(
        "earthchem.resources",
        "soap_search_schema.xsd")

# Mapping XML types to our simple types
TYPE_MAPPING = {
    '{http://www.w3.org/2001/XMLSchema}complexType': 'complex',
    '{http://www.w3.org/2001/XMLSchema}simpleType': 'simple',
    '{http://www.w3.org/2001/XMLSchema}string': 'string',
    'xs:string': 'string'
}

# Mapping for namespaces
_NS = {"xs": "http://www.w3.org/2001/XMLSchema"}

def get_type(elem):
    """ Get the data type for an XML element
    """    
    # First check the attributes
    attrtype = elem.get('type')
    if attrtype is not None:
        return TYPE_MAPPING[attrtype]

    # Ok so there's probably some children to check then
    # If we have children then we can have a complex type or a simple type
    # If an xs:complexType we make a dict, if xs:simpleType we expect a string
    for child in elem.getchildren():
        try:
            return TYPE_MAPPING[child.tag]
        except KeyError:
            continue
    
    # If we're here we dont' know what to do
    raise ValueError("Can't parse type for element named {}".format(elem.get('name')))

def complex_validator(elem):
    """ Construct a validator for an xs:complexType
    """
    # Pull together keys and validators for each key
    validators = {}
    for attr in elem.xpath('./xs:complexType/xs:attribute', namespaces=_NS):
        # Decide what type of validator we need based on attribute type
        attrtype = get_type(attr)
        if attrtype == 'string':
            # We accept anything for strings
            validators[name] = string_validator(attr)
            
        elif attrtype == 'simple':
            # For simple types there's a restriction on values
            print('constructing simple validator')
            validators[attr.get('name')] = construct_simple_validator(attr)
            
        elif attrtype == 'complex':
            validators[attr.get('name')] = construct_complex_validator(attr)
        
    # Construct a validator function
    name = elem.get('name')
    def _validator(obj):
        if type(obj) != dict:
            raise ValueError('I expected a dict for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))
        
        # Check keys and values against schema
        for key, value in obj.items():
            try:
                vd = validators[key]
            except KeyError:
                raise KeyError('Unknown key {} - valid values are {}'.format(key, list(validators.keys())))
    
    return _validator

def simple_validator(elem):
    """ Construct a validator for an xs:simpleType - these are normally values
        with particular restrictions
    """
    # Construct a validator that checks values against known ok values
    name = elem.get('name')
    def _validator(obj):
        if type(obj) != dict:
            raise ValueError('I expected a str for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))

    # Return the validation function
    return _validator

def string_validator(elem):
    """ String validator for objects - validates any string it's passed
    """
    # Construct a validator that just checks that we have a string
    name = elem.get('name')
    def _validator(obj):
        if type(obj) != str:
            raise ValueError('I expected a string for parameter {} - got a {} instead ({})'.format(elem, type(obj), obj))
        return True
    
    # Return the validation function
    return _validator

VALIDATOR_MAPPING = {
    'string': string_validator,
    'complex': complex_validator,
    'simple': simple_validator
}

def validate(dict_like, validators):
    for key, value in dict_like.items():
        try:
            if not validators[key](value):
                raise ValueError
        except KeyError:
            print('Invalid key {}, valid keys are {}'.format(key, validators.keys()))
        print(validators[key](value))

class QueryElement(dict):
    
    """ Class to generate a query element for each 
        part of the query
        
        This generates fairly kludgy validators against 
        the SOAP search schema which will let us check that
        a query is well-formed.
        
        Parameters:
            name - the name of the query element.
                Should be the same as in the XML soap
                search schema.
    """
    
    def __init__(self, name):
        self.name = name.lower()
        self.xmlname = name
        
        # Storage slots for caching
        self._tree = None
        
        # Find the element for the given name
        query = "//xs:element[@name='{}']".format(self.xmlname)
        self.root = self.xpath(query)[0]
        self.dtype = get_type(self.root)
        if self.dtype == 'complex':
            print('getting valid keys')
            print('getting valid values')
        elif self.dtype == 'simple':
            print('getting valid values')
        else:
            print('Query is just a string')
    
    @property
    def tree(self):
        "Return the XML tree for the SOAP schema"
        # Return from cache if we already have it
        if self._tree is not None:
            return self._tree
        
        # Otherwise just make a new tree
        with open(SOAP_SCHEMA, 'r') as src:
            self._tree = etree.parse(src)
        
        return self._tree
    
    def xpath(self, query):
        "Run an xpath query against our schema"
        return self.tree.xpath(query, namespaces=_NS)
