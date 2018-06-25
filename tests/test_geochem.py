import unittest
import pandas as pd
import numpy as np
import periodictable as pt
from earthchem.geochem import to_weight, to_molecular, common_elements, \
                              REE


class TestWeightMolarReversal(unittest.TestCase):
    """Tests the reversability of weight-molar unit transformations."""

    def setUp(self):
        self.df = pd.DataFrame({'MgO':20.0, 'SiO2':30.0, 'K2O':5.0, 'Na2O':2.0},
                               index=[0])
        self.components = ['MgO', 'SiO2', 'K2O']

    def test_weightmolar_reversal_renormFalse(self):
        """
        Tests reversability of the wt-mol conversions.
        Examines differences between dataframes, and
        asserts that any discrepency is explained by np.nan components
        (and hence not actual differences).
        """
        M = to_molecular(self.df.loc[:, self.components],
                                          renorm=False)
        W = to_weight(self.df.loc[:, self.components],
                                          renorm=False)

        W_M = to_weight(M, renorm=False)
        M_W = to_molecular(W, renorm=False)

        # Where values are not close, it's because of nans
        W_M_close = np.isclose(W_M.values,
                                self.df.loc[:, self.components].values)
        self.assertTrue(np.isnan(W_M.values[~W_M_close]).all())

        M_W_close = np.isclose(M_W.values,
                                self.df.loc[:, self.components].values)
        self.assertTrue(np.isnan(M_W.values[~M_W_close]).all())


class TestCommonElements(unittest.TestCase):
    """Tests the common element generator."""

    def test_cutoff(self):
        """Check the function works normal cutoff Z numbers."""
        for cutoff in [1, 15, 34, 63, 93]:
            with self.subTest(cutoff=cutoff):
                self.assertTrue(common_elements(cutoff=cutoff)[-1].number==cutoff)

    def test_high_cutoff(self):
        """Check the function works silly high cutoff Z numbers."""
        for cutoff in [119, 1000, 10000]:
            with self.subTest(cutoff=cutoff):
                self.assertTrue(len(common_elements(cutoff=cutoff))<130)
                self.assertTrue(common_elements(cutoff=cutoff)[-1].number<cutoff)

    def test_formula_output(self):
        """Check the function produces formula output."""
        for el in common_elements(cutoff=10, output='formula'):
            with self.subTest(el=el):
                self.assertIs(type(el), type(pt.elements[0]))

    def test_string_output(self):
        """Check the function produces string output."""
        for el in common_elements(cutoff=10, output='string'):
            with self.subTest(el=el):
                self.assertIs(type(el), str)


class TestREE(unittest.TestCase):
    """Tests the Rare Earth Element generator."""

    def setUp(self):
        self.min_z = 57
        self.max_z = 71

    def test_complete(self):
        """Check all REE are present."""
        reels = REE(output='formula')
        ns = [el.number for el in reels]
        for n in range(self.min_z, self.max_z + 1):
            with self.subTest(n=n):
                self.assertTrue(n in ns)

    def test_precise(self):
        """Check that only the REE are returned."""
        reels = REE(output='formula')
        ns = [el.number for el in reels]
        self.assertTrue(min(ns) == self.min_z)
        self.assertTrue(max(ns) == self.max_z)

    def test_formula_output(self):
        """Check the function produces formula output."""
        for el in REE(output='formula'):
            with self.subTest(el=el):
                self.assertIs(type(el), type(pt.elements[0]))

    def test_string_output(self):
        """Check the function produces string output."""
        for el in REE(output='string'):
            with self.subTest(el=el):
                self.assertIs(type(el), str)
