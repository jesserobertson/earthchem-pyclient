from earthchem.query import RESTClientQuery

import unittest

class TestRESTClientData(unittest.TestCase):

    def setUp(self):
        self.query = RESTClientQuery(author='barnes')
        self.count = self.query.count()
        self.df = self.query.dataframe()

    def test_data_type(self):
        "Check the right columns are numeric"
        # Expected dtypes for columns here
        expected = {
            'float64': [
                'al2o3', 'cao', 'cl', 'feot', 'k', 'k2o', 'latitude', 'longitude', 'mgo', 'mno', 'na2o', 'p2o5', 'sio2', 'tio2'
            ],
            'object': [
                'author', 'composition', 'journal', 'material', 'method', 'rock_name', 'sample_id', 'source', 'title', 'type'
            ]
        }

        for dtype, keys in expected.items():
            for key in keys:
                try:
                    self.assertEqual(str(self.df[key].dtype), dtype)
                except KeyError:
                    pass

if __name__ == '__main__':
    unittest.main()