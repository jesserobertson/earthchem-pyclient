""" file:   test_transforms.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017

    description: Unit tests for our transform implementations
"""

import unittest
import numpy as np
from scipy import stats

np.random.seed(42)  # don't forget your towel

from earthchem.transform.isometric import IsometricLogTransform
from earthchem.transform.centered import CenteredLogTransform
from earthchem.transform.barycentric import BarycentricTransform
from earthchem.transform.additive  import AdditiveLogTransform
from earthchem.transform.utilities import basis_matrix, closure

def ortho_group(dim, size=1):
    """
    Draw random samples from O(N).

    Stolen from scipy v. 18 code cause we don't have it here yet

    Parameters:
        dim - the dimension of rotation space (N).
        size - the number of samples to draw (default 1).

    Returns:
        Random size N-dimensional matrices, dimension (size, dim, dim)
    """
    size = int(size)
    if size > 1:
        return np.array([ortho_group(dim) for i in range(size)])

    H = np.eye(dim)
    for n in range(1, dim):
        x = stats.norm.rvs(size=(dim-n+1,))

        # random sign, 50/50, but chosen carefully to avoid roundoff error
        D = np.sign(x[0])
        x[0] += D * np.sqrt((x * x).sum())

        # Householder transformation
        Hx = -D * (np.eye(dim - n + 1)
                   - 2 * np.outer(x, x) / (x * x).sum())
        mat = np.eye(dim)
        mat[n-1:, n-1:] = Hx
        H = np.dot(H, mat)
    return H

def correlation_matrix(ndim, distribution=None):
    """
    Generate a random correlation matrix

    Parameters:
        ndim - the number of dimensions in the matrix
        distribution - optional, a scipy.stats distribution to
            generate eigenvalues from (random eigenvalues must
            be positive). Defaults to scipy.stats.gamma(1)

    Returns:
        a random correlation matrix
    """
    # Specify the eigenvalue distribution
    dist = distribution or stats.gamma(1)

    # Generate random rotation
    D = np.diag(dist.rvs(ndim))
    Q = ortho_group(ndim)
    return np.dot(np.dot(Q, D), Q.T)

class TestTransforms(unittest.TestCase):

    "Unit tests for transforms"

    def test_centered_logratio_isometry(self):
        "Centered logratio should be isomorphic under closure"
        t = CenteredLogTransform()

        # Loop over different dimensions
        npts = 1000
        for ndim in (3, 5, 10, 20):
            for _ in range(10):
                # Generate random variables
                mvn = stats.multivariate_normal(
                            mean=stats.uniform(0, 1).rvs(ndim),
                            cov=correlation_matrix(ndim, stats.gamma(2))
                            )

                X = t.inverse_transform(mvn.rvs(npts))
                L = t.transform(X)

                # Check that things are the right size
                self.assertEqual(X.shape, (npts, ndim))
                self.assertEqual(L.shape, (npts, ndim))

                # Check that inverse and transform are isomorphic#
                # Need to use pre-transformed variables since these are
                # only isomorphic to closure
                self.assertTrue(np.allclose(X, t.inverse_transform(L)))
                self.assertTrue(np.allclose(L, t.transform(X)))

    def test_barycentric_isometry(self):
        "Centered logratio should be isomorphic under closure"
        t = BarycentricTransform()

        # Loop over different dimensions
        npts = 1000
        for _ in range(10):
            # Generate random variables
            mvn = stats.multivariate_normal(
                stats.uniform(0, 1).rvs(3),
                correlation_matrix(3, stats.gamma(2)))
            X = mvn.rvs(npts)
            L = t.transform(X)

            # Check that things are the right size
            self.assertEqual(X.shape, (npts, 3))
            self.assertEqual(L.shape, (npts, 2))

    def test_barycentric_error(self):
        "Passing data with ndims != 3 should raise a ValueError"
        t = BarycentricTransform()

        # Loop over different dimensions
        for ndim in (2, 4, 5, 10, 20):
            # Generate random variables
            mvn = stats.multivariate_normal(
                stats.uniform(0, 1).rvs(ndim),
                correlation_matrix(ndim, stats.gamma(2)))
            self.assertRaises(ValueError, t.transform, mvn.rvs(10))

    def test_isometric_basis_matrix(self):
        "ILR basis matrix should be constructed correctly"
        for ndim in range(2, 20):
            psi = basis_matrix(ndim)

            # Check that Q @ Q.T = identity
            self.assertTrue(
                np.allclose(np.dot(psi, psi.T),
                            np.identity(ndim - 1)))

            # Check that Q.T @ Q = identity - 1 / D * ones
            expected = np.identity(ndim) - np.ones((ndim, ndim)) / ndim
            self.assertTrue(np.allclose(np.dot(psi.T, psi),
                                        expected))

    def test_closure(self):
        "Closure operator should work ok"
        for ndim in range(2, 20):
            for npts in (10, 100, 1000):
                mvn = stats.multivariate_normal(stats.uniform(0, 1).rvs(3),
                                        correlation_matrix(3, stats.gamma(2)))
                X = closure(mvn.rvs(npts))
                self.assertTrue(np.allclose(X.sum(axis=1), np.ones(npts)))

    def test_isometric_logratio_isometry(self):
        "Isometric logratio should be isomorphic under closure"
        t = IsometricLogTransform()

        # Loop over different dimensions
        npts = 1000
        for ndim in (3, 5, 10, 20):
            for _ in range(10):
                # Generate random variables
                mvn = stats.multivariate_normal(
                    stats.uniform(0, 1).rvs(ndim - 1),
                    correlation_matrix(ndim - 1))
                X = t.inverse_transform(mvn.rvs(npts))
                L = t.transform(X)

                # Check that things are the right size
                self.assertEqual(X.shape, (npts, ndim))
                self.assertEqual(L.shape, (npts, ndim - 1))

                # Check that inverse and transform are isomorphic#
                # Need to use pre-transformed variables since these are
                # only isomorphic to closure
                self.assertTrue(np.allclose(X, t.inverse_transform(L)))
                self.assertTrue(np.allclose(L, t.transform(X)))

    def test_additive_logratio_isometry(self):
        "Additive logratio should be isomorphic under closure"
        t = AdditiveLogTransform()

        # Loop over different dimensions
        npts = 1000
        for ndim in (3, 5, 10, 20):
            for _ in range(10):
                # Generate random variables
                mvn = stats.multivariate_normal(
                    stats.uniform(0, 1).rvs(ndim - 1),
                    correlation_matrix(ndim - 1))
                X = t.inverse_transform(mvn.rvs(npts))
                L = t.transform(X)

                # Check that things are the right size
                self.assertEqual(X.shape, (npts, ndim))
                self.assertEqual(L.shape, (npts, ndim - 1))

                # Check that inverse and transform are isomorphic#
                # Need to use pre-transformed variables since these are
                # only isomorphic to closure
                self.assertTrue(np.allclose(X, t.inverse_transform(L)))
                self.assertTrue(np.allclose(L, t.transform(X)))

    def test_additive_logratio_isometry_with_specd_scale(self):
        "Additive logratio should be isomorphic under closure"
        # Loop over different dimensions
        npts = 1000
        for ndim in (3, 5, 10, 20):
            for _ in range(10):
                t = AdditiveLogTransform(np.random.randint(0, ndim))

                # Generate random variables
                mvn = stats.multivariate_normal(
                    stats.uniform(0, 1).rvs(ndim - 1),
                    correlation_matrix(ndim - 1))
                X = t.inverse_transform(mvn.rvs(npts))
                L = t.transform(X)

                # Check that things are the right size
                self.assertEqual(X.shape, (npts, ndim))
                self.assertEqual(L.shape, (npts, ndim - 1))

                # Check that inverse and transform are isomorphic#
                # Need to use pre-transformed variables since these are
                # only isomorphic to closure
                self.assertTrue(np.allclose(X, t.inverse_transform(L)))
                self.assertTrue(np.allclose(L, t.transform(X)))

    def test_additive_index_error(self):
        "Additive logratio should raise value error if base index > len"
        ndim = 4
        mvn = stats.multivariate_normal(
            stats.uniform(0, 1).rvs(ndim - 1),
            correlation_matrix(ndim - 1))
        alr = AdditiveLogTransform(ndim + 2)
        clr = CenteredLogTransform()
        X = clr.inverse_transform(mvn.rvs(1000))
        self.assertRaises(ValueError, alr.transform, X)

if __name__ == '__main__':
    unittest.main()
