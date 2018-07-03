import unittest

import pandas as pd
import numpy as np
from numpy.random import multivariate_normal
import ternary
import matplotlib.axes as matax

from earthchem.plot import ternaryplot, spiderplot, densityplot
from earthchem.geochem import common_elements, REE


class TestSpiderplot(unittest.TestCase):
    """Tests the Spiderplot functionality."""

    def setUp(self):
        reels = REE(output='string')
        self.df = pd.DataFrame({k: v for k,v in zip(reels,
                                np.random.rand(len(reels), 10))})

    @unittest.expectedFailure
    def test_noplot_nofill(self):
        """Test failure on no-plot no-fill options."""
        spiderplot(self.df, plot=False, fill=False)

    @unittest.expectedFailure
    def test_invalid_style_options(self):
        """Test stability under invalid style values."""
        style = {'color': 'notacolor', 'marker': 'red'}
        spiderplot(self.df, **style)


class TestTernaryplot(unittest.TestCase):
    """Tests the Ternaryplot functionality."""

    def setUp(self):
        self.cols = ['MgO', 'CaO', 'SiO2']
        self.df = pd.DataFrame({k: v for k,v in zip(self.cols,
                                np.random.rand(len(self.cols), 10))})

    def test_none(self):
        """Test generation of plot with no data."""
        df = pd.DataFrame(columns=self.cols)
        out = ternaryplot(df)
        self.assertEqual(type(out),
                         ternary.ternary_axes_subplot.TernaryAxesSubplot)


    def test_one(self):
        """Test generation of plot with one record."""
        df = self.df.head(1)
        out = ternaryplot(df)
        self.assertEqual(type(out),
                         ternary.ternary_axes_subplot.TernaryAxesSubplot)

    def test_multiple(self):
        """Test generation of plot with multiple records."""
        df = self.df.loc[:, :]
        out = ternaryplot(df)
        self.assertEqual(type(out),
                         ternary.ternary_axes_subplot.TernaryAxesSubplot)


class TestDensityplot(unittest.TestCase):
    """Tests the Densityplot functionality."""

    def setUp(self):
        self.cols = ['MgO', 'SiO2', 'CaO']
        data = np.array([0.5, 0.4, 0.3])
        cov =   np.array([[2, -1, -0.5],
                         [-1, 2, -1],
                         [-0.5, -1, 2]])
        bidata = multivariate_normal(data[:2], cov[:2, :2], 2000)

        self.bidf = pd.DataFrame(bidata, columns=self.cols[:2])
        tridata = multivariate_normal(data, cov, 2000)
        self.tridf = pd.DataFrame(tridata, columns=self.cols)

    def test_modes(self):
        """Tests different ploting modes."""
        for df in [self.bidf, self.tridf]:
            with self.subTest(df=df):
                for mode in ['density', 'hist2d', 'hexbin']:
                    with self.subTest(mode=mode):
                        out = densityplot(df, mode=mode)
                        self.assertTrue(isinstance(out, matax.Axes))


if __name__ == '__main__':
    unittest.main()
