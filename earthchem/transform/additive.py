""" file:   additive.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: Additive log transform for pipelines
"""

import re

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from .utilities import closure, pd_closure

class AdditiveLogTransformPandas(BaseEstimator, TransformerMixin):

    """ A custom sklearn transformer which implements an additive log ratio
        transformatino for compositional data.

        Works nicely with Pandas dataframes

        Parameters:
            constant - the constant to use for inverse transforms (defaults tp
                unity, i.e. fractions)
            base_feature_pattern - a regular expression matching the key of the 
                base feature column
    """

    def __init__(self, constant=1, base_feature_pattern=".*_unmeasured"):
        self.constant = constant
        self.patt = re.compile(base_feature_pattern)
        self._base_key = None

    def fit(self, X, y=None):
        """
        Fit does nothing
        """
        return self
        
    def transform(self, X):
        """
        Push dataframe through ALR using unmeasured column to normalize
        
        Parameters:
            X - the DataFrame to transform

        Returns:
            a dataframe with transformed data, will be missing the 
            'unmeasured' column since that's been normalized out.
        """
        # Order the existing keys
        self._base_key = [k for k in X.keys() if self.patt.match(k)][0]
        others = sorted([k for k in X.keys() if self.patt.match(k) is None])

        # Calculate and return ALR'd columns
        return X[others].apply(lambda x: np.log(x / X[unmeasured_key]))

    def inverse_transform(self, X):
        """
        Push dataframe through inverse additive logratio
        
        Assumes that the missing column is 'unmeasured', see documentation for
        additive logratio transform.
        
        Parameters:
            df - the data to transform
            constant - the constant for calculating closure
        
        Returns:
            a dataframe with untransformed data, will have the closure column
            labelled 'unmeasured'
        """
        output = X.apply(np.exp)
        output_key = (self._base_key if self._base_key is not None 
                      else 'closure')
        output[output_key] = np.ones((X.shape[0], 1))
        return pd_closure(output, self.constant)


class AdditiveLogTransform(BaseEstimator, TransformerMixin):
    
    """ A custom sklearn transformer which implements an additive log ratio 
        transformation for nD compositional data
    """

    def __init__(self, base_feature_index=1):
        """
        Initialize the transform using the first feature to normalize

        Parameters:
            base_feature_index - which feature to use to normalize the ratios.
                Optional, defaults to 0 (the first feature)
        """
        self.base_feature_index = base_feature_index

    def fit(self, X, *args, **kwargs):
        """
        Fit does nothing here
        """
        return self

    def transform(self, X):
        """ 
        Returns the additive log ratio transform of the given composition vectors X

        Parameters:
            X - an array of composition vectors. An M x N array where M 
                is the number of samples, and N is the number of 
                compositional species. 

        Returns:
            the additive log ratio-transformed data L
        """
        try:
            X = np.asarray(X)
            ratios = (X.T / X[:, self.base_feature_index]).T
            ratios = np.delete(ratios, self.base_feature_index, axis=1)
            return np.log(ratios)
        except IndexError:
            msg = ('Input data has no base feature index at {}'
                   ', probably because there are not enough features. '
                   'Maybe try setting a different base_feature_index?')
            raise ValueError(msg.format(self.base_feature_index))
   
    def inverse_transform(self, L):
        """ 
        Returns the inverse additive log ratio transformed data
    
        Parameters:
            Parameters:
                L - an array of CLR-transformed composition vectors. 
        
        Returns:
            the inverted data X
        """
        L = np.asarray(L)
        npoints, ndim = L.shape

        # Need to put in extra column in right place!
        if self.base_feature_index == 0:
            result = np.hstack([np.zeros((npoints, 1)), L])
        elif self.base_feature_index in {-1, ndim}:
             result = np.hstack([L, np.zeros((npoints, 1))])
        else:
            result = np.hstack([
                L[:, :self.base_feature_index], 
                np.zeros((npoints, 1)), 
                L[:, self.base_feature_index:]
            ])

        # Return closure of result
        return closure(np.exp(result))
