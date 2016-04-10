#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from core.classifier import match

app = Flask(__name__, static_url_path='')


def get_team_list():
    return [(1, 'IND'), (2, 'AUS'), (3, 'SRL'), (4, 'NZL'), (5, 'SAC')]

def get_player_list(country1, country2):
    return [[(1, 'Raina'), (2, 'Dhawan'), (3, 'Kholi'), (4, 'Dhoni'), (5, 'Yuvraj')],
    [(11, 'Watson'), (12, 'Dude1'), (13, 'Dude2'), (14, 'Dude3'), (15, 'Dude4')]]

@app.route('/', methods = ['GET'])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/home', methods = ['GET'])
def home():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    teams = get_team_list()
    if request.method == "GET":
        return render_template('predict.html', teams=teams)
    if request.method == "POST":
        player_order = request.get_json(force=True)["playerOrder"]
        player_order = [903,905,904,912,902,911,906,908,917,901,910,1009,1005,1008,1015,1002,1012,1001,1003,1004,1013,1011]
        vec2 = [1215,1203,1201,1202,1212,1216,1207,1213,1208,1211,1210,308,305,1211,309,301,302,307,310,303,304,312]
        clf = match.Classify(n_neighbors=1)
        probab = clf.predict_outcome(player_order)
        print(probab[0][0])
        return jsonify(country_1=probab[0][0], country_2=probab[0][1])

@app.route('/profile', methods = ['GET', 'POST'])
def analyse():
    if request.method == "GET":
        return render_template('profile.html')

@app.route('/getplayers', methods = ['GET'])
def getplayers():
    if request.method == "GET":
        country1 = request.args.get('country1')
        country2 = request.args.get('country2')
        print(country1)
    return jsonify(data=get_player_list(country1, country2))

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
