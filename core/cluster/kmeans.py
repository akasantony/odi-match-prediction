from sklearn.cluster import KMeans as km
import csv
from config import paths
import pprint
import json

__authors__ = "Akas Antony"
__email__ = "antony.akas@gmail.com"
__date__ = "14th, November 2015"


class KMeans(object):
    def __init__(self, cl_num):
        self.kmeans = km(n_clusters=cl_num)

    def fit(self, vec):
        self.kmeans.fit(vec)
        self.centroids = self.kmeans.cluster_centers_
        return self.kmeans.labels_


def extract_vec(csv_file):
    vect = []
    player_id = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vect.append([float(row['NumOfInningsBatted']), float(row['NotOutInnings']), float(row['Bat_AVG']),
                        float(row['Bat_SR']), float(row['MRA']), float(row['BRPI']), float(row['HS']), float(row['NumOfIngsBowled']),
                        float(row['BW_AVG']), float(row['BW_SR']), float(row['BW_ECN']), float(row['MDO']), float(row['HW'])])
            player_id.append(row['player_id'])
    return player_id, vect

if __name__ == '__main__':
    json_dump = open(paths.__KCLUSTERLABELS__, 'w')
    pp = pprint.PrettyPrinter(indent=4)
    cl = KMeans(9)
    playerid, vec = extract_vec(paths.__VECTORS__+'player.csv')
    labels = cl.fit(vec)
    dic = {}
    for index, label in enumerate(labels):
        dic.setdefault(str(label), []).append(playerid[index])
    pprint.pprint((dic))
    json.dump(dic, json_dump)
