from earthchem import Query

import unittest

class TestRESTClientQuery(unittest.TestCase):

    "Tests for RESTClient"

    def setUp(self):
        self.query = Query()

    def test_set_author(self):
        "Check that author setting works ok"
        for auth in ('smith', 'barnes'):
            self.query['author'] = auth
            self.assertEqual(self.query['author'], auth)
            self.assertEqual(self.query.url, 
                             'http://ecp.iedadata.org/restsearchservice?outputtype=json&author={}'.format(auth))
            self.assertEqual(repr(self.query),
                             'Query(author={})'.format(auth))

    def test_author_count(self):
        "Check that we handle author counts when things are 0"
        self.query['author'] = 'aqwefgaskl'
        self.assertEqual(self.query.count(), 0)
        self.assertEqual(self.query.dataframe(), None)

    def test_author_count_with_data(self):
        "Check things work with an author count that returns data"
        self.query['author'] = 'barnes'
        self.assertTrue(self.query.count() > 5)
        self.assertTrue(self.query.dataframe() is not None)

    def test_borked_key(self):
        "Check that an unknown key raises an error"
        with self.assertRaises(KeyError):
            self.query['asdfjkl'] = 'asdfh'

    def test_remove(self):
        "Check that removing a key works ok"
        self.query['searchtype'] = 'rowdata'
        self.assertEqual(self.query['searchtype'], 'rowdata')
        self.query['searchtype'] = None
        with self.assertRaises(KeyError):
            _ = self.query['searchtype']

if __name__ == '__main__':
    unittest.main()