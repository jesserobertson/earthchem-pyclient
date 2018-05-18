""" file:   requests.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Pagination utilities
"""

from itertools import takewhile, count

def make_pages(max_items, items_per_page=50):
    """ Get a list of page bounds for submitting to the REST endpoint
        
        Parameters:
            max_items - the total number of items to get
            items_per_page - the size of each page (defaults to 50 which is 
                the Earthchem default)
        
        Returns:
            a list of tuples with (start_row, end_row) for each page
    """
    # Make a list of page bounds until we get bigger than the maximum number of items
    page_bounds = lambda n: (n * items_per_page, (n + 1) * items_per_page - 1)
    pages = list(takewhile(lambda x: x[0] < max_items, 
                           map(page_bounds, count())))

    # Replace last value with maximum row number
    pages[-1] = (pages[-1][0], max_items)
    return pages