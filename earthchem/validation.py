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
    
    # If we're here we will just assume that the type is 'string'
    return TYPE_MAPPING['xs:string']

# Mapping simple types to our validator factories
# Note we have to actually define these below once we've defined the functions
# as part of this mapping
VALIDATOR_MAPPING = {}

def complex_validator(elem):
    """ Construct a validator for an xs:complexType
    """
    # Pull together keys and validators for each key
    attributes = elem.xpath('./xs:complexType/xs:attribute', namespaces=_NS)
    validators = {
        attr.get('name'): VALIDATOR_MAPPING[get_type(attr)](attr)
        for attr in attributes
    }

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
        return True
    
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
        return True

    # Return the validation function
    return _validator

def string_validator(elem):
    """ String validator for objects - validates any string it's passed
    """
    # Construct a validator that just checks that we have a string
    name = elem.get('name')
    def _validator(obj):
        if type(obj) != str:
            raise ValueError('I expected a string for parameter {} - got a {} instead ({})'.format(name, type(obj), obj))
        return True
    
    # Return the validation function
    return _validator

# Mapping simple types to our validator factories
VALIDATOR_MAPPING = {
    'string': string_validator,
    'complex': complex_validator,
    'simple': simple_validator
}

class ElementValidator(dict):
    
    """ Class to generate a query validator for each 
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
        self._validator = VALIDATOR_MAPPING[self.dtype](self.root)
    
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

    def validate(self, obj):
        """ Validate a python object against the schema

            Parameters:
                obj - the object to validate 
        """
        return self._validator(obj)
