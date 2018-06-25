""" file:   barycentric.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: barycentric transform for pipelines
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class BarycentricTransform(BaseEstimator, TransformerMixin):
    
    """ A custom sklearn transformer which implements a barycentric 
        transformation for 3D compositional data
    """

    def fit(self, X, y=None):
        """
        Fit does nothing
        """
        return self
        
    def transform(self, X):
        """ 
        Returns the barycentric transform of the given composition vectors X

        Parameters:
            X - a Nx3 array containing the data to transform into barycentric 
                coordinates

        Returns:
            the barycentric-transformed data
        """
        X = np.asarray(X)
        if X.shape[-1] != 3:
            raise ValueError('X has wrong dimension for barycentric coords')
        x0, x1, x2 = X.transpose()
        denom = np.asarray(2*(x0 + x1 + x2), dtype=np.float)
        return np.array([(2*x1 + x2) / denom, np.sqrt(3)*x2 / denom]).T