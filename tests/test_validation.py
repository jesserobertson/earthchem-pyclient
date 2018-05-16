from earthchem.validation import QueryElement

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


if __name__ == '__main__':
    unittest.main()