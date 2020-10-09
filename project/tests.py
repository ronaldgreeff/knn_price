import unittest

import numpy as np
from clusterer import ClusterControl


class TestClusterControl(unittest.TestCase):

    def setUp(self):

        X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80], [95, 105], [105, 95], [100, 100] ])
        tcis = ([0, 1], [2, 3], [5, 6, 7]) # list of X indices that should form true clusters

        self.tcis = tcis
        self.X = X
        self.CC = ClusterControl(X, tcis, 1)

    def test_get_min_max_eps_for_cluster(self):

        tci = self.tcis[0]
        min_samples = len(tci)

        min_eps, max_eps = self.CC.get_min_max_eps_for_cluster(tci, min_samples)

        self.assertEqual(min_eps, 5)
        self.assertEqual(max_eps, 15)

    def test_get_cluster_boundaries(self):

        self.CC.get_cluster_boundaries()
        self.assertEqual(self.CC.all_eps, type(list()))

    # def test_set_min_max(self):
    #
    #     self.CC.set_min_max()
    #     self.assertEqual(self.CC.min_eps, 5)
    #     self.assertEqual(self.CC.max_eps, 15)

    # def test_get_labelled_data(self):
    #
    #     # eps = (min_eps+max_eps)/2 # {0: ['a', 'a'], 1: ['p', 'p'], -1: ['o'], 2: ['t', 't']}
    #     # labels = C.get_labelled_data(eps, min_samples)
    #     t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']
    #     # print(C.map_labels_by_cluster(t_labels, labels))
    #
    #     self.assertEqual(t_labels, 1)


if __name__ == '__main__':
    unittest.main()
