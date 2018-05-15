from earthchem.requests import RESTClientQuery

import unittest

class TestRESTClientQuery(unittest.TestCase):

    "Tests for RESTClient"

    def setup(self):
        query = RESTClientQuery()

    def test_set_author(self):
        "Check that author setting works ok"
        query['author'] = 'smith'
        self.assertEqual(query['author'], 'smith')
        self.assertEqual(query.url, '')

if __name__ == '__main__':
    unittest.main()