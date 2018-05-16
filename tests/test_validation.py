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
            elem = ElementValidator(element)
            self.assertTrue(elem is not None)
            self.assertTrue(elem.tree is not None)
            del elem

    def test_validator_creation_1(self):
        "Elements should create their own validators"
        for element in ELEMENTS_IN_SCHEMA:
            elem = ElementValidator(element)
            self.assertTrue(elem.validator is not None)
            del elem

    def test_validator_creation_2(self):
        "Check that complex validators work ok"
        elem = ElementValidator('Reference')
        validator = complex_validator(elem.root)

        # Check validator
        works = {'author': 'barnes', 'journal': 'nature'}
        self.assertTrue(validator(works))
        b0rks = works.copy()
        b0rks['foo'] = 'bar'
        with self.assertRaises(KeyError):
            validator(b0rks)


if __name__ == '__main__':
    unittest.main()