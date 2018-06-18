import pandas as import pd
import periodictable as pt


def common_elements(cutoff=92, output='formula'):
    """
    Provides a list of elements up to a particular cutoff (default: including U)
    Output options are 'formula', or strings.
    """
    elements = [el for el in pt.elements
                if not (el.__str__() == 'n' or el.number>cutoff)]
    if not output == 'formula':
        elements = [el.__str__() for el in elements]
    return elements
