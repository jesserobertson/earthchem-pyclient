""" file:   requests.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Handles requests against EarthChem's API
"""

from .documentation import get_documentation

import textwrap

def make_query_docstring():
    """ Constructs a docstring from the documentation dictionary
    """
    wrapper = textwrap.TextWrapper(width=80, subsequent_indent='    ')
    docstr = textwrap.dedent("""
        Holds a query for the EarthChem REST API

        Initialize by providing key-value pairs to build into a query URL. The
        URL is available in the `url` attribute, and the results from the
        `results` attribute.

        Providing a keyword not in the list below will raise a KeyError.

        Allowed keywords are:
        """)
    docdict = get_documentation()
    for item in docdict.items():
        docstr += '\n' + wrapper.fill('{0} - {1}'.format(*item))
    return docstr

class RESTClientQuery(dict):

    __doc__ = make_query_docstring()
    docdict = get_documentation()

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            # Check that items are ok to query
            if key not in self.docdict.keys():
                raise KeyError('Unknown key {0}'.format(key))

            # Add to dictionary
            self[key] = str(value)

    def __setitem__(self, key, value):
        """ Sets a particular query term, making sure that the values 
            are ok etc. 
            
            Parameters:
                key - the query key to set
                value - the value to set for that search.
        """
        if value is None:
            del self[key]
        else:
            super().__setitem__(key, value)

    @property
    def url(self):
        query_string = ('http://ecp.iedadata.org/restsearchservice?'
                        'outputtype=json')
        for item in self.items():
            query_string += '&{0}={1}'.format(*item)
        return query_string

    @property
    def result(self):
        """ Query the webservice using the current query
        """
        # Make a call to the webservice
        pass
    
    def info(self, key, pprint=True):
        """ Return info about a search key
        
            Parameters:
                key - the key to get information about
                pprint - whether to print the information or return 
                    a dictionary with the contents
                
            Returns:
                if pprint=True, None, otherwise a dictionary with a
                'doc' string and a 'valid_values' 
        """
        pass
