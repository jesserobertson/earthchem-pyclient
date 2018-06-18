from earthchem import Query

from matplotlib import pyplot as plt

import unittest

class IntegrationTestRESTClientQuery(unittest.TestCase):
    "Some integration tests to check that things are working"

    def setUp(self):
        self.query = Query(author='barnes')
        self.df = self.query.dataframe()

    def test_plot_latlon(self):
        "Check that plotting works without any issues"
        self.df.plot('longitude', 'latitude', 'scatter')
        plt.close()

    def test_plot_data(self):
        "Check that plotting works with data inputs"
        self.df.plot('al2o3', 'sio2', 'scatter')
        plt.close()

if __name__ == '__main__':
    unittest.main()
