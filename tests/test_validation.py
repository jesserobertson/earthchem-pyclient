from earthchem.validation import *

import unittest

ELEMENTS_IN_SCHEMA = (
    'Reference',
    'SampleType',
    'SampleID',
    'Keyword',
    'CruiseID',
    'Location',
    'Age',
    'Material'
)

class TestValidators(unittest.TestCase):

    "Test validators"

    def test_integration(self):
        "Elements should build for all elements in the schema"
        for element in ELEMENTS_IN_SCHEMA:
            elem = QueryElement(element)
            self.assertTrue(elem is not None)
            self.assertTrue(elem.tree is not None)
            del elem

    def test_validator_creation(self):
        for element in ('Reference',):
            elem = QueryElement(element)
            validator = complex_validator(elem.root)
            del elem


if __name__ == '__main__':
    unittest.main()