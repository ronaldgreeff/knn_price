from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt



class DbscanObj:

    def __init__(self, eps=0, min_samples=1):
        self.obj = DBSCAN(eps, min_samples)

    def _new_dbscan_model(self, X):
        self.obj.fit(X)

    def set_eps(self, eps):
        self.obj.eps = eps


class ClusterControl:

    def __init__(self, X, tcis, step=0.00001):

        self.X = X
        self.tcis = tcis
        self.step = step
        self.min_eps = 0
        self.max_eps = 0
        self.dbscan_obj = self._new_dbscan_obj()


    def _new_dbscan_obj(self, eps=0, min_samples=1):
        return DbscanObj(eps, min_samples)


    def get_min_max_eps_for_cluster(self, tci, min_samples):
        """ new dbscan instance with eps 0
        tci (truth cluster indices) - indices of X data that form a known cluster
        increase eps by step
        all tci datapoints in a single cluster - min
        keep increasing eps by step until
        a non tci datapoint is included minus 1 step - max
        """
        eps = self.step

        dbscan = self._new_dbscan_obj(eps=eps, min_samples=min_samples)
        dbscan._new_dbscan_model(self.X)

        # labels = []
        cluster_labels = []
        # keep going until cluster labels all == 1
        while len(set(cluster_labels)) != 1:
            dbscan.eps = eps
            labels = dbscan.obj.labels_
            #                                        ignore outliers
            cluster_labels = [labels[i] for i in tci if labels[i] >=0]
            eps += self.step
            print(eps)

        min_eps = eps

        label = set(tci_labels).pop()

        while list(labels).count(label) <= min_samples:
            dbscan.eps = eps
            labels = model.labels_
            eps += self.step

        max_eps = eps

        return min_eps, max_eps


    def get_cluster_boundaries(self):

        self.all_eps = []

        for tci in self.tcis:

            min_samples = len(tci)

            min_eps, max_eps = self.get_min_max_eps_for_cluster(tci, min_samples)

            self.min = min_eps if (min_eps < self.min and self.min != 0) else 0
            self.max = max_eps if (max_eps < self.max and self.max != 0) else 0

            self.all_eps.append((min_eps, max_eps))


    def get_labelled_data(self, eps, min_samples):
        """ Using the pre-caclulated eps, get labelled clusters from the data
        """
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        model = dbscan.fit(X)

        return model.labels_

    def map_labels_by_cluster(self, t_labels, labels):
        d = {}
        for i, label in enumerate(labels):
            if d.get(label):
                d[label].append(t_labels[i])
            else:
                d[label] = [t_labels[i]]
        return d


if __name__ == '__main__':

    pass
    # todo: move this into test
    # X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95] ])
    # t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']
    #
    # true_cluster_indices = [2, 3]
    # min_samples = len(true_cluster_indices)
    #
    # C = clusterer()
    # min_eps, max_eps = C.get_cluster_boundaries(X, true_cluster_indices, min_samples)
    # eps = (min_eps+max_eps)/2 # {0: ['a', 'a'], 1: ['p', 'p'], -1: ['o'], 2: ['t', 't']}
    # labels = C.get_labelled_data(eps, min_samples)
    # print(C.map_labels_by_cluster(t_labels, labels))
    #
    #
    # # dbscan = DBSCAN(eps = 10, min_samples = 2)
    # # model = dbscan.fit(X)
    # # labels = model.labels_
    # plt.figure()
    # plt.scatter(X[:,0], X[:,1])
    # plt.show()
