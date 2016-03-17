#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__, static_url_path='')


def get_team_list():
	return [(1, 'IND'), (2, 'AUS'), (3, 'SRL'), (4, 'NZL'), (5, 'SAC')]

def get_player_list(country1, country2):
	return [[(1, 'jaja'), (2, 'masi'), (3, 'taru'), (4, 'koke'), (5, 'saru')],
	[(11, 'asdf'), (12, 'qwe'), (13, 'sdf'), (14, 'sdg'), (15, 'bmbn')]]

@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == "GET":
		return render_template('index.html')

@app.route('/home', methods = ['GET', 'POST'])
def home():
	if request.method == "GET":
		return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	teams = get_team_list()
	if request.method == "GET":
		return render_template('predict.html', teams=teams)

@app.route('/analyse', methods = ['GET', 'POST'])
def analyse():
	if request.method == "GET":
		return render_template('analyse.html')

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
