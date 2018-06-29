import unittest
import pandas as pd
from earthchem.formatting import cleanup_dataframe


class TestCleanupDataFrame(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'sample_Id':20.0, 'sio2':30.0, 'K2O':5.0,
                                'Na2o':2.0, 'cs': 14, 'location': 'Lima, Peru'},
                               index=[0])

    def test_capitalisation(self):
        """Test capitalisation of dataframe columns."""

        outdf = cleanup_dataframe(self.df)
        cols = list(outdf.columns)
        check_lowercase = [x[0]==x[0].lower() for x in cols]
        self.assertFalse(any(check_lowercase))

    def test_chemcolumns(self):
        outdf = cleanup_dataframe(self.df)
        cols = list(outdf.columns)
        for chem in ['SiO2', 'K2O', 'Na2O', 'Cs']:
            with self.subTest(chem=chem):
                self.assertIn(chem, cols)


    def test_reordering(self):
        """Test reordering of dataframe columns."""
        outdf = cleanup_dataframe(self.df)
        cols = list(outdf.columns)
        check_cols = ['SampleID', 'SiO2', 'Cs']
        idx = [cols.index(c) for c in cols]
        # Check the sorting is right
        self.assertTrue(all(idx[i] <= idx[i+1] for i in range(len(idx)-1)))


if __name__ == '__main__':
    unittest.main()
