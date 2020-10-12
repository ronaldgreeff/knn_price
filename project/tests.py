import unittest
import numpy as np
from clusterer import get_min_eps_for_cluster, get_max_eps_for_cluster, get_cluster_boundaries


class TestClusterControl(unittest.TestCase):

    def test_get_min_eps_for_cluster(self):
        X = np.array([[1, 2], [2, 2], [2, 3]])
        tci = [0, 1, 2]
        min_samples = len(tci) # since we expect tcis to represent a unique element per page/sample
        step = 0.01

        result = get_min_eps_for_cluster(X, tci, min_samples, step)

        self.assertEqual(result, 1.0)


    def test_get_max_eps_for_cluster(self):
        X = np.array([[1, 0], [1, 0], [5, 0]])
        tci = [0, 1]
        min_samples = len(tci)
        step = 0.01

        result = get_max_eps_for_cluster(X, tci, min_samples, step, label=0, eps=1.0,)

        self.assertEqual(result, 4.0)


    def test_get_cluster_boundaries(self):

        X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80], [95, 105], [105, 95], [100, 100] ])
        tcis = ([0, 1], [2, 3], [5, 6, 7]) # list of X indices that should form true clusters

        result = get_cluster_boundaries(X, tcis)


if __name__ == '__main__':
    unittest.main()
