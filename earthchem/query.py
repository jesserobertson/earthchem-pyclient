""" file:   requests.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Handles requests against EarthChem's API
"""

from .documentation import get_documentation

import requests
import pandas

from io import StringIO
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

class Query(dict):

    __doc__ = make_query_docstring()
    docdict = get_documentation()

    def __init__(self, **kwargs):
        super().__init__()

        # Add everything to dictionary
        for key, value in kwargs.items():
            # Add to dictionary
            self[key] = str(value)

    def __repr__(self):
        kwargs = ', '.join('{0}={1}'.format(*it) for it in self.items())
        return 'Query({})'.format(kwargs)

    def __setitem__(self, key, value):
        """ Sets a particular query term, making sure that the values 
            are ok etc. 
            
            Parameters:
                key - the query key to set
                value - the value to set for that search.
        """
        # Check that items are ok to query
        if key not in self.docdict.keys():
            raise KeyError('Unknown key {0}'.format(key))

        if value is None:
            del self[key]
        else:
            super().__setitem__(key, value)

    def count(self):
        """ Get the total number of items returned by the query
        """
        self['searchtype'] = 'count'
        resp = requests.get(self.url)
        # del self['searchtype']

        # Return the result
        if resp.ok:
            try:
                return int(resp.json()['Count'])
            except:
                raise IOError("Couldn't parse data in response")
        else:
            raise IOError("Couldn't get data from network") 

    def dataframe(self, standarditems=True, drop_empty=True):
        """ Get the actual data in a dataframe

            Note that this doesn't do pagination yet...

            Parameters:
                standarditems - if True, returns the Earthchem 
                    standard items in the table
                drop_empty - if True, drops columns for which there 
                    is no data
        """
        # Add the proper search type keys to the query
        self['searchtype'] = 'rowdata'
        self['standarditems'] = 'yes' if standarditems else 'no'
        resp = requests.get(self.url)
        self['searchtype'], self['standarditems'] = None, None

        # Return the result
        if resp.ok:
            try:
                # Create a dataframe
                df = pandas.read_json(StringIO(resp.text))

                # Convert numerical values
                string_values = {  # things to keep as strings
                    'sample_id', 'source', 'url', 'title', 'author', 'journal',
                    'method', 'material', 'type', 'composition', 'rock_name'
                }
                for key in df.keys():
                    if key not in string_values:
                        df[key] = pandas.to_numeric(df[key])

                # Drop empty columns
                if drop_empty:
                    df.dropna(axis='columns', how='all', inplace=True)
                return df

            except ValueError:
                if resp.text == 'no results found':
                    print("Didn't find any records, returning None")
                    return None
                else:
                    raise IOError("Couldn't parse data in response")
        else:
            raise IOError("Couldn't get data from network")

    @property
    def url(self):
        query_string = ('http://ecp.iedadata.org/restsearchservice?'
                        'outputtype=json')
        for item in self.items():
            query_string += '&{0}={1}'.format(*item)
        return query_string
    
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
