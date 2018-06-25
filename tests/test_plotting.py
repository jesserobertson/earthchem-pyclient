import unittest

import pandas as pd
import numpy as np
import ternary

from earthchem.plot import ternaryplot, spiderplot
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

    def test_irrellevant_style_options(self):
        """Test stability under additional kwargs."""
        style = {'thingwhichisnotacolor': 'notacolor', 'irrelevant': 'red'}
        self.assertWarns(UserWarning, spiderplot(self.df, **style))

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

if __name__ == '__main__':
    unittest.main()
