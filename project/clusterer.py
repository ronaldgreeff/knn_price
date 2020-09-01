from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

class clusterer:
    # def __init__(self, df):
    #     self.npa = df.to_numpy()

    def get_cluster_boundaries(self):#, X, true_cluster_indices):
        """ Determine the min and max eps to use, using partially labelled data
            Reasoning:
            A single product title will be present on each `Page` dataframe. If you
            stack Pages, Titles should be there own cluster. min_samples therefor
            == len(Pages) or len(rows with label "Title") / a list of
            true_cluster_indices. You can then calc the min_eps (the val needed
            for each value "Title" datapoint to be within a single cluster)
            and the max_eps (the val a step before the cluster includes something
            other than a "Title" datapoint)
        """

        # t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']
        true_cluster_indices = [2, 3]
        X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95] ])

        eps = 0.01
        steps = 0.01

        min_eps = 0
        max_eps = 0
        min_samples = len(true_cluster_indices)
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

    def get_labelled_data(self):
        """ Using the pre-caclulated eps, get labelled clusters from the data """
        min_samples = 2
        a = 7.089999999999893 # [ 0  0  1  1 -1 -1 -1] * t cluster includes outlier
        c = 32.0300000000022 # [0 0 1 1 1 2 2] * m cluster includes outlier
        b = ((a+b)/2) # [ 0  0  1  1 -1  2  2] * the midpoint seems like a good starting point
        X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95] ])
        dbscan = DBSCAN(eps=c, min_samples=min_samples)
        model = dbscan.fit(X)
        print(model.labels_)

class labeller:
    pass


if __name__ == '__main__':

    C = clusterer()
    # min_eps, max_eps = C.get_cluster_boundaries()
    # eps = (min_eps+max_eps)/2
    C.get_labelled_data()

    # dbscan = DBSCAN(eps = 10, min_samples = 2)
    # model = dbscan.fit(X)
    # labels = model.labels_
    # plt.figure()
    # plt.scatter(X[:,0], X[:,1])
    # plt.show()
