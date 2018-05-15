""" file:   documentation.py (earthchem)
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Scraping the Earthchem site for documentation etc
"""

import requests
from bs4 import BeautifulSoup

from collections import OrderedDict
import pkg_resources
import re
import textwrap

def strip_whitespace(string):
    """ Strip newline, tab and multple whitespace from a string
    """
    return re.sub(' +', ' ',
                  string.replace('\n', ' ').replace('\t', ' ').strip())


# Construct request from EarthChem rest documentation
REST_DOCO_URL = 'http://ecp.iedadata.org/rest_search_documentation/'
if not requests.get(REST_DOCO_URL).ok:
    # We can just use the cached version
    CACHED_DOCO_FILE = pkg_resources.resource_stream(
        "earthchem.resources",
        "earthchem_rest_search_documentation.html")
    REST_DOCO_URL = 'file://' + str(CACHED_DOCO_FILE)

# Keys to ignore when constructing the query class
IGNORE_VALUES = (
    re.compile('Example.*'),
    re.compile('level[0-9]')
)

def get_documentation():
    """ Get query items and documentaton by scraping the EarthChem rest
        documentation
    """
    # Hit the endpoint
    response = requests.get(REST_DOCO_URL)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
    else:
        raise IOError("Can't find Earthchem REST documentation")

    # Parse me some documentation
    docs = OrderedDict()
    for item in soup.select('.itemtitle'):
        # Check that we actually want to keep this value
        itemname = strip_whitespace(item.contents[0])
        if any(map(lambda regex: regex.match(itemname),
                   IGNORE_VALUES)):
            continue

        # Parse document string, add to dictionary
        itemdoc = strip_whitespace(item.contents[1].contents[0])
        docs[itemname] = itemdoc

    return docs
