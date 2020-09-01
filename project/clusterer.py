from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

class clusterer:
    # def __init__(self, df):
    #     self.npa = df.to_numpy()

    def get_params(self, np_array, true_cluster_indices):
        """ truth labels holds the index of 1 set of clustered labels """

        # start at a low eps
        # set min samples equal to len(true_cluster_indices)
        # draw clusters
        # while len of set(labels at true_cluster_indices) > 1:
        #   increase eps by small amount
        # once len is 1, set the min_eps value
        # while the occurences of true_cluster labels < len true_cluster_indices:
        #   set max_eps
        #   increase eps by small amount

        eps = 0.01
        min_eps = 0
        max_eps = 0
        min_samples = len(true_cluster_indices)
        labels = []
        tci_labels = []

        while len(set(tci_labels)) != 1:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            model = dbscan.fit(X)
            labels = model.labels_
            eps += 0.01
            tci_labels = [labels[i] for i in true_cluster_indices if labels[i] >= 0]

        min_eps = eps
        label = set(tci_labels).pop()

        while list(labels).count(label) <= len(true_cluster_indices):
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            model = dbscan.fit(X)
            labels = model.labels_
            eps += 0.01

        max_eps = eps

        print(min_eps, max_eps)


if __name__ == '__main__':

    t_labels = ['a', 'a', 'p', 'p', 'o', 't', 't']
    true_cluster_indices = [2, 3]
    X = np.array([ [10, 5], [5, 10], [50, 55], [55, 50], [70, 80],[95, 105], [105, 95] ])

    clusterer().get_params(X, true_cluster_indices)

    # dbscan = DBSCAN(eps = 10, min_samples = 2)
    # model = dbscan.fit(X)
    # labels = model.labels_
    # plt.figure()
    # plt.scatter(X[:,0], X[:,1])
    # plt.show()
