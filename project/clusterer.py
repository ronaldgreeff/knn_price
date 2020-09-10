from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

class clusterer:
    # def __init__(self, df):
    #     self.npa = df.to_numpy()

    def get_cluster_boundaries(self, X, true_cluster_indices, min_samples):
        """ Determine the min and max eps to use, using partially labelled data
            Reasoning:
            A single product title will be present on each `Page` dataframe. If you
            stack Pages, Titles should be there own cluster. min_samples therefor
            == len(Pages) or len(rows with label "Title") / a list of
            true_cluster_indices. You can then calc the min_eps (the val needed
            for each value "Title" datapoint to be within a single cluster)
            and the max_eps (the val a step before the cluster includes something
            other than a "Title" datapoint)

            todo: this could be made more accurate by using more labels, e.g. price
            or sale_price. Resolve for min and max eps from all clusters.
        """

        eps = 0.01
        steps = 0.01

        min_eps = 0
        max_eps = 0
        tci_labels = []
        labels = []

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)

        # len tci_labels will init with 0 and then be >1. We want to make it 1.
        while len(set(tci_labels)) != 1:
            dbscan.eps = eps
            model = dbscan.fit(X)
            labels = model.labels_
            #                                                     ignore outliers
            tci_labels = [labels[i] for i in true_cluster_indices if labels[i] >= 0]
            eps += steps

        min_eps = eps
        label = set(tci_labels).pop()

        # check the model labels for the occurences of label. Increment eps
        # until an additional datapoint is added to the label cluster
        while list(labels).count(label) <= len(true_cluster_indices):
            dbscan.eps = eps
            model = dbscan.fit(X)
            labels = model.labels_
            eps += steps

        max_eps = eps

        return min_eps, max_eps

    def get_labelled_data(self, eps, min_samples):
        """ Using the pre-caclulated eps, get labelled clusters from the data """
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

    # todo: move this into test

    X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95] ])
    t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']

    true_cluster_indices = [2, 3]
    min_samples = len(true_cluster_indices)

    C = clusterer()
    min_eps, max_eps = C.get_cluster_boundaries(X, true_cluster_indices, min_samples)
    eps = (min_eps+max_eps)/2 # {0: ['a', 'a'], 1: ['p', 'p'], -1: ['o'], 2: ['t', 't']}
    labels = C.get_labelled_data(eps, min_samples)
    print(C.map_labels_by_cluster(t_labels, labels))


    # dbscan = DBSCAN(eps = 10, min_samples = 2)
    # model = dbscan.fit(X)
    # labels = model.labels_
    plt.figure()
    plt.scatter(X[:,0], X[:,1])
    plt.show()
