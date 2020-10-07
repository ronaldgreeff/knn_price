import unittest

import numpy as np
from clusterer import ClusterControl


class TestClusterControl(unittest.TestCase):

    def setUp(self):
        self.CC = ClusterControl()
        self.X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95], [100, 100] ])
        self.tci_list = ([0, 1], [2, 3], [5, 6, 7]) # list of X indices that should form true clusters

    def test_get_boundaries_for_single_cluster(self):
        """ Given a list of datapoints in format ([a,b], [a,b]) calc the min and max
            eps for each cluster.

            Assumes that each datapoint is a unique element amongst the elements of
            that dataset - num datapoints in list above == min samples.

            Min eps is eps needed to cluster all a given cluster's datapoints.
            Max eps is eps minus 1 var step value.
        """
        tci = self.tci_list[0]
        min_samples = len(tci)
        self.CC._new_dbscan_obj(min_samples)
        # min_samples = len(true_cluster_indices)
        min_eps, max_eps = self.CC.get_min_eps_for_cluster(tci)

        # eps = (min_eps+max_eps)/2 # {0: ['a', 'a'], 1: ['p', 'p'], -1: ['o'], 2: ['t', 't']}
        # labels = C.get_labelled_data(eps, min_samples)

        t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']
        # print(C.map_labels_by_cluster(t_labels, labels))

        # result = clusterer.clusterer.get_cluster_boundaries(X, true_cluster_indices, min_samples)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()
