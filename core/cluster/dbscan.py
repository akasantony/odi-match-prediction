from sklearn.cluster import DBSCAN
import csv
from config import paths
from matplotlib import pyplot
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer
from sklearn.decomposition import PCA
import numpy as np
from sklearn.externals import joblib


class Cluster(object):
    def __init__(self, eps=1.8, min_samples=1):
        self.db = DBSCAN(eps=eps, min_samples=min_samples)

    def fit(self, vec):
        vec = StandardScaler().fit_transform(vec)
        self.db.fit(vec)
        return self.db.fit_predict(vec)

    def extract_vec(self, match_csv, squad_csv, player_csv):
        vec = []
        match_id = []
        squad_order = []
        class_label = []
        player_vec = {}
        with open(squad_csv, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                squad_order.append([int(row["slot1"]), int(row["slot2"]), int(row["slot3"]), int(row["slot4"]), int(row["slot5"]),
                int(row["slot6"]), int(row["slot7"]), int(row["slot8"]), int(row["slot9"]), int(row["slot10"]), int(row["slot11"]),
                int(row["slot21"]), int(row["slot22"]), int(row["slot23"]), int(row["slot24"]), int(row["slot25"]), int(row["slot26"]),
                int(row["slot27"]), int(row["slot28"]), int(row["slot29"]), int(row["slot30"]), int(row["slot31"])])
        with open(player_csv, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                player_vec[int(row["player_id"])] = [float(row["NumOfInningsBatted"]), float(row["NotOutInnings"]), float(row["Bat_AVG"]),
                float(row["Bat_SR"]), float(row["MRA"]), float(row["BRPI"]), float(row["HS"]), float(row["NumOfIngsBowled"]), float(row["BW_AVG"]),
                float(row["BW_SR"]), float(row["BW_ECN"]), float(row["MDO"]), float(row["HW"])]
        squad_vec = self.__player_dim_reduction(squad_order, player_vec)
        with open(match_csv, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                vec.append([int(row["score1"]), int(row["balls_faced1"]), int(row["extra_runs1"]),
                            int(row["wickets1"]), int(row["score2"]), int(row["balls_faced2"]),
                            int(row["extra_runs2"]), int(row["wickets2"])])
                vec[index] += squad_vec[index]
                win_team = int(row["win_team"])
                if win_team == int(row["team1"]):
                    class_label.append(1)
                if win_team == int(row["team2"]):
                    class_label.append(0)
                match_id.append(row["match_id"])
        return match_id, class_label, vec

    def __player_dim_reduction(self, squad_order, player_vec):
        keys = []
        vec = []
        transformed_squad = []
        for key in player_vec.keys():
            keys.append(key)
            vec.append(player_vec[key])
        X = np.array(vec)
        pca = PCA(n_components=1)
        pca.fit(X)
        joblib.dump(pca, paths.__MODELS__+'pca.pkl')
        transformed_vec = pca.transform(X)
        for match in squad_order:
            x = []
            for player in match:
                x.append(transformed_vec[keys.index(player)][0])
            transformed_squad.append(x)
        return transformed_squad

if __name__ == '__main__':
    cl = Cluster(eps=6, min_samples=1)
    match_id, class_label, vec = cl.extract_vec(paths.__VECTORS__+'match.csv', paths.__VECTORS__+'team_squad.csv', paths.__VECTORS__+'player.csv')
    print(type(vec))
    x = []
    y = []
    for i in vec:
        x.append(i[0])
        y.append(i[1])
    pyplot.scatter(x, y)
    pyplot.savefig('plot.png')
    cluster_labels = list(cl.fit(vec))
    n_clusters_ = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    x = sorted(list(zip(match_id, vec, cluster_labels, class_label)), key=lambda a: int(a[2]))
    d = {}
    for temp_id, temp_vec, temp_cluster, temp_class in x:
        d.setdefault(temp_id, []).append(temp_vec)
    f = open(paths.__VECTORS__+'match_cluster.csv', 'w', newline='')
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["match_id","match_vec","cluster_label","win_label"])
    writer.writerows(x)
