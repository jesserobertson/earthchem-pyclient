""" file:   isometric.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: Isometric log transform for pipelines
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from .utilities import basis_matrix, closure

class IsometricLogTransform(BaseEstimator, TransformerMixin):
    
    """ A custom sklearn transformer which implements centered-log scaling
        for compositional data
    """

    def fit(self, X, y=None):
        """
        Fit does nothing
        """
        return self

    def transform(self, X):
        """ 
        Returns the isometric log ratio transform of the given composition vectors X

        Parameters:
            X - an array of composition vectors. An M x N array where M 
                is the number of samples, and N is the number of 
                compositional species. 

        Returns:
            the additive log ratio-transformed data L
        """
        X = np.asarray(X)
        psi = basis_matrix(X.shape[1])
        return np.dot(np.log(X), psi.T)
   
    def inverse_transform(self, L):
        """ 
        Returns the inverse isometric log ratio transformed data
    
        Parameters:
            Parameters:
                L - an array of ILR-transformed composition vectors. 
        
        Returns:
            the inverted data X
        """
        L = np.asarray(L)
        psi = basis_matrix(L.shape[1] + 1)
        return closure(np.exp(np.dot(L, psi)))