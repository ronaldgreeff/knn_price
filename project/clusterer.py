from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

def get_min_eps_for_cluster(X, tci, min_samples, step):

    tci_labels = set()
    eps = step

    while True:
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
        tci_labels = set([clustering.labels_[i] for i in tci if clustering.labels_[i] >=0])

        if len(tci_labels) == 1:
            return round(eps, 5)

        eps += step


def get_max_eps_for_cluster(X, tci, min_samples, step, label, eps):

    while True:
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
        label_occurences = list(clustering.labels_).count(label)

        print(eps, clustering.labels_, label_occurences)

        if label_occurences > min_samples:
            return round((eps - step), 5)

        eps += step

def get_cluster_boundaries(self):
    pass

    # def get_cluster_boundaries(self):
    #
    #     self.all_eps = []
    #
    #     for tci in self.tcis:
    #
    #         min_samples = len(tci)
    #
    #         min_eps, max_eps = self.get_min_max_eps_for_cluster(self.X, tci, min_samples)
    #
    #         self.min = min_eps if (min_eps < self.min and self.min != 0) else 0
    #         self.max = max_eps if (max_eps < self.max and self.max != 0) else 0
    #
    #         self.all_eps.append((min_eps, max_eps))
    #
    #
    # def get_labelled_data(self, eps, min_samples):
    #     """ Using the pre-caclulated eps, get labelled clusters from the data
    #     """
    #     dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    #     model = dbscan.fit(X)
    #
    #     return model.labels_
    #
    # def map_labels_by_cluster(self, t_labels, labels):
    #     d = {}
    #     for i, label in enumerate(labels):
    #         if d.get(label):
    #             d[label].append(t_labels[i])
    #         else:
    #             d[label] = [t_labels[i]]
    #     return d


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
