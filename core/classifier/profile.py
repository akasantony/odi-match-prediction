from sklearn.neighbors import KNeighborsClassifier
from core.config import paths
import json
import csv
from scipy import spatial
import copy


class Cluster(object):
    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.labels = json.load(open(paths.__KCLUSTERLABELS__, 'r'))
        self.vect = []
        self.player_id = []
        with open(paths.__VECTORS__+'player.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.vect.append([float(row['NumOfInningsBatted']), float(row['NotOutInnings']), float(row['Bat_AVG']),
                            float(row['Bat_SR']), float(row['MRA']), float(row['BRPI']), float(row['HS']), float(row['NumOfIngsBowled']),
                            float(row['BW_AVG']), float(row['BW_SR']), float(row['BW_ECN']), float(row['MDO']), float(row['HW'])])
                self.player_id.append(row['player_id'])

    def __fit(self, X, y):
        self.knn.fit(X, y)

    def __extract_labels(self):
        X = []
        y = []
        for key in self.labels.keys():
            X.append(self.labels[key])
            y.append(key)
        return X, y

    def __id2vec(self, player_ids, clus_labels):
        N = copy.deepcopy(player_ids)
        m = copy.deepcopy(clus_labels)
        X = []
        y = []
        for ind_i, i in enumerate(N):
            for ind_j, j in enumerate(i):
                X.append((j, self.vect[self.player_id.index(j)]))
                y.append(m[ind_i])
        return X, y

    def __sim_cluster(self, label, X ,y ):
        vec = []
        for ind_i, i in enumerate(y):
            if i == label:
                vec.append(X[ind_i])
        return vec

    def __cosine(self, sim_vec, vec):
        sim_dist = []
        for i in sim_vec:
            sim_dist.append(spatial.distance.euclidean(i, vec))
        return sim_dist

    def __normalize(self, vec, slice_value=5):
        sorted_list = sorted(vec, key=lambda x: x[1])
        sorted_list = sorted_list[-slice_value:]
        sum_list = sum(i[1] for i in sorted_list)
        sorted_list = [(x[0], (x[1]/sum_list)*100) for x in sorted_list]
        return sorted_list

    def __predict_label(self, vec):
        player_ids, clus_labels = self.__extract_labels()
        X, y = self.__id2vec(player_ids, clus_labels)
        temp_X = []
        for i in X:
            temp_X.append(i[1])
        self.__fit(temp_X, y)
        return self.knn.predict([vec]), X, y

    def __get_player_vec(self, pl_id):
        print(self.player_id)
        return self.vect[self.player_id.index(str(pl_id))]

    def get_sim_players(self, pl_id):
        vec = self.__get_player_vec(pl_id)
        print(vec)
        label, X, y = self.__predict_label(vec)
        sim_vec = self.__sim_cluster(label, X, y)
        temp_sim_vec = []
        temp_sim_label = []
        for i in sim_vec:
            temp_sim_vec.append(i[1])
            temp_sim_label.append(i[0])
        dist = self.__cosine(temp_sim_vec, vec)
        vec_dist = zip(temp_sim_label, dist)
        return self.__normalize(vec_dist)

if __name__ == '__main__':
    prf = Cluster()
