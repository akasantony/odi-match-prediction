from sklearn.cluster import DBSCAN
import csv
from config import paths
from matplotlib import pyplot
from sklearn.preprocessing import StandardScaler


class Cluster(object):
    def __init__(self, eps=1.8, min_samples=1):
        self.db = DBSCAN(eps=eps, min_samples=min_samples)

    def fit(self, vec):
        vec = StandardScaler().fit_transform(vec)
        self.db.fit(vec)
        return self.db.fit_predict(vec)


def extract_vec(csv_file):
    vec = []
    match_id = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vec.append([int(row["score1"]), int(row["balls_faced1"]), int(row["extra_runs1"]),
                        int(row["wickets1"]), int(row["score2"]), int(row["balls_faced2"]),
                        int(row["extra_runs2"]), int(row["wickets2"])])
            match_id.append(row["match_id"])
        return match_id, vec

if __name__ == '__main__':
    cl = Cluster(eps=2, min_samples=1)
    match_id, vec = extract_vec(paths.__VECTORS__+'match.csv')
    x = []
    y = []
    for i in vec:
        x.append(i[0])
        y.append(i[1])
    pyplot.scatter(x, y)
    pyplot.savefig('plot.png')
    labels = list(cl.fit(vec))
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    x = sorted(list(zip(match_id, labels)), key=lambda a: int(a[1]))
    d = {}
    for v, k in x:
        d.setdefault(k, []).append(v)
    print(vec)
    print(d)
    f = open(paths.__VECTORS__+'match_cluster.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(x)



