import csv
from config import paths
import numpy as np
from sklearn import svm
from core.config import paths
from sklearn.externals import joblib


__authors__ = "Akas Antony"
__email__ = "antony.akas@gmail.com"
__date__ = "21st, March 2016"

class Classify(object):
    def __init__(self, n_neighbors=3):
        self.clf = svm.SVC(probability=True, kernel='rbf')
        self.pca = joblib.load(paths.__MODELS__+'pca.pkl')

    def __extract_vecs(self, match_csv):
        X = []
        y = []
        with open(match_csv, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                vec = eval(row["match_vec"])
                X.append(vec[-22:])
                y.append(int(row["win_label"]))
        return X, y

    def __convert_lineup(self, player_order):
        vec = []
        with open(paths.__VECTORS__+'player.csv') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                if int(row["player_id"]) in player_order:
                    player_order[player_order.index(int(row["player_id"]))] = [float(row["NumOfInningsBatted"]), float(row["NotOutInnings"]), float(row["Bat_AVG"]),
                    float(row["Bat_SR"]), float(row["MRA"]), float(row["BRPI"]), float(row["HS"]), float(row["NumOfIngsBowled"]), float(row["BW_AVG"]),
                    float(row["BW_SR"]), float(row["BW_ECN"]), float(row["MDO"]), float(row["HW"])]
        for i in player_order:
            if i != 'NaN':
                vec.append(self.pca.transform([i])[0][0])
            else:
                vec.append(np.nan)
        return vec

    def __get_sim_matches(self, label):
        X = []
        y = []
        with open(paths.__VECTORS__+'match_cluster.csv') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                if int(row["cluster_label"]) == label:
                    X.append(eval(row["match_vec"])[-22:])
                    y.append(int(row["win_label"]))
            return X, y

    def __match_outcome(self, X, y, vec):
        self.clf.fit(X, y)
        return self.clf.predict_proba(vec)

    def predict_outcome(self, player_order):
        conv_vec = self.__convert_lineup(player_order)
        X, y = self.__extract_vecs(paths.__VECTORS__+'match_cluster.csv')
        label = self.__match_outcome(X, y, [conv_vec])
        print(label)
        return label

if __name__ == '__main__':
    cl = Classify(n_neighbors=1)
    vec = [1215,1203,1201,1202,1212,1216,1207,1213,1208,1211,1210,308,305,1211,309,301,302,307,310,303,304,312]
    cl.predict_outcome(vec)
