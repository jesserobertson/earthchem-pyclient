from earthchem import pagination

import unittest

TEST_DATA = [
    # input, expected output
    ([200], [(0, 49), (50, 99), (100, 149), (150, 200)]),
    ([159], [(0, 49), (50, 99), (100, 149), (150, 159)]),
    ([149, 30], [(0, 29), (30, 59), (60, 89), (90, 119), (120, 149)]),
    ([1], [(0, 1)])
]

class TestPagination(unittest.TestCase):

    def test_pagination_function(self):
        for ipt, expected in TEST_DATA:
            self.assertEqual(expected, pagination.make_pages(*ipt))

if __name__ == '__main__':
    unittest.main()