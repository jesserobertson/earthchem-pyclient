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
SOAP_SCHEMA = pkg_resources.resource_stream(
        "earthchem.resources",
        "soap_search_schema.xsd")

# Mapping XML types to our simple types
TYPE_MAPPING = {
    '{{{}}}complexType'.format(self.ns['xs']): 'complex',
    '{{{}}}simpleType'.format(self.ns['xs']): 'simple',
    '{{{}}}string'.format(self.ns['xs']): 'string',
    'xs:string': 'string'
}

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
    raise ValueError("Can't parse type for element {}".format(elem))

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
    
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    
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
        with open(soap_schema, 'r') as src:
            self._tree = etree.parse(src)
        
        return self._tree
    
    def xpath(self, query):
        "Run an xpath query against our schema"
        return self.tree.xpath(query, namespaces=self.ns)
