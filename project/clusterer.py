from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

class clusterer:
    def __init__(self, df):
        self.npa = df.to_numpy()

    def get_params(self, truth_labels):
        """ truth labels holds the index of 1 set of clustered labels """

        eps = 0.01
        labels_confirmed = []
        while len(labels_confirmed) < len(truth_labels):
            dbscan = DBSCAN(eps=eps, min_samples=len(truth_labels))


if __name__ == '__main__':

    X = np.array([ [1, 2], [2, 2], [7, 6], [8, 7], [2, 3], [25, 8] ])
    dbscan = DBSCAN(eps = 3, min_samples = 2)
    model = dbscan.fit(X)
    labels = model.labels_

    plt.figure()
    plt.scatter(X[:,0], X[:,1])
    plt.show()
