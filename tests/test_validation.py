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

TEST_EXAMPLES = {
    'Reference': {
        'works': [
            {'author': 'barnes', 'journal': 'nature'},
            {'author': 'barnes', 'journal': 'nature', 'doi': 'foo'},
            {'author': 'klump'},
            {'exactpubyear': '2005'},
            {'minpubyear': '2000', 'maxpubyear': '2017'}
        ],
        'fails': [
            (ValueError, ['foo', 'bar']),
            (ValueError, 'a string'),
            (KeyError, {'a':'dict', 'with': 'random', 'keys': 'fails'})
        ]
    },
    # 'SampleType',
    # 'SampleID',
    # 'Keyword',
    # 'CruiseID',
    # 'Location',
    # 'Age',
    # 'Material'
}

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
            self.assertTrue(elem._validator is not None)
            del elem

    def test_validator_creation_2(self):
        "Check that complex validators work ok"
        for name, cases in TEST_EXAMPLES.items():
            v = ElementValidator(name)
            for case in cases['works']:
                self.assertTrue(v.validate(case))
            for errtype, case in cases['fails']:
                with self.assertRaises(errtype):
                    v.validate(case)


if __name__ == '__main__':
    unittest.main()