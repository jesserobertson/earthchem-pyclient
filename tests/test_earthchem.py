from earthchem.query import RESTClientQuery

import unittest

class TestRESTClientQuery(unittest.TestCase):

    "Tests for RESTClient"

    def setUp(self):
        self.query = RESTClientQuery()

    def test_set_author(self):
        "Check that author setting works ok"
        for auth in ('smith', 'barnes'):
            self.query['author'] = auth
            self.assertEqual(self.query['author'], auth)
            self.assertEqual(self.query.url, 'http://ecp.iedadata.org/restsearchservice?outputtype=json&author={}'.format(auth))


if __name__ == '__main__':
    unittest.main()