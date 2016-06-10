#!/usr/bin/python

"""" This script is used to interface between the backend and frontend of the application """

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from core.classifier import profile as prf
from core.classifier import UI_interface_inputs
import pymysql
from collections import Counter

app = Flask(__name__, static_url_path='')

cnx = pymysql.connect("localhost","root","root","cricketcommentaryanalysis")
mycursor = cnx.cursor()

def find_role(lis):
	print(lis)
	role = []
	for each in lis:
		role.append(each[-1])

	words_to_count = (word for word in role if word[:1].isupper())
	c = Counter(words_to_count)
	return(c.most_common(2))



def update_data(name, country, playerrole, battingrole, bowlingrole):
    query = """select * from player_card where country='%s'"""%(country)
    try:
        mycursor.execute(query)
        res = mycursor.fetchall()
        prev_player_id = res[-1][0]
        player_id = prev_player_id+1
        print(player_id, name)
        insert_query = """insert into player_card values('%d', '%s', '%s', '%s',
        '%s', '%s')"""%(player_id, country, name, playerrole, battingrole, bowlingrole)
        mycursor.execute(insert_query)
        cnx.commit()
    except:
        print("Unable to process transaction.")

def get_team_list():
    query = """select * from teams"""
    mycursor.execute(query)
    results = mycursor.fetchall()
    return results

def get_player_list(country1, country2):
    print(country1)
    query1 = """select player_id, player_name, playing_role from player_card where country='%s'"""%(country1)
    query2 = """select player_id, player_name, playing_role from player_card where country='%s'"""%(country2)
    mycursor.execute(query1)
    results1 = mycursor.fetchall()
    mycursor.execute(query2)
    results2 = mycursor.fetchall()
    print(results1, results2)
    return [results1, results2]

def suggested_players(query):
    query  = """select * from player_card where player_name like '%%"""+query+"""%%'"""
    try:
        mycursor.execute(query)
        results = mycursor.fetchall()
        vec =[]
        for eachEntry in results:
            vec.append({"label":eachEntry[2], "indx": eachEntry[0]})
    except:
        print("Error: Unable to fetch Data")
    return vec

def id2player(val):
    print(val)
    vec =[]
    for i in val:
        query = """select * from player_card where player_id="""+str(i[0])
        try:
            mycursor.execute(query)
            results = mycursor.fetchall()
            for eachEntry in results:
                vec.append([i[1], eachEntry[1], eachEntry[2], eachEntry[3]])
        except:
            print("Error: Unable to fetch Data")
    return vec


def sim_players(pl_id):
    pr = prf.Cluster()
    sim_ind = pr.get_sim_players(pl_id)
    return id2player(sim_ind)

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
        print(player_order)
        ts_win_probab, tc_win_probab, StrengthAnalysis = UI_interface_inputs.inningsPredictionValue(player_order)
        print(ts_win_probab, tc_win_probab)
        return jsonify(setting=ts_win_probab, chasing=tc_win_probab, strength=StrengthAnalysis)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if request.method == "GET":
        return render_template('profile.html')
    if request.method == "POST":
        plyr_id = request.get_json(force=True)["player_id"]
        data = sim_players(plyr_id)
        role = find_role(data)
        X={}
        X["data"]=data
        X["role"]=role
        print(X["role"])
        return jsonify(data=X)

@app.route('/getplayers', methods = ['GET'])
def getplayers():
    if request.method == "GET":
        country1 = request.args.get('country1')
        country2 = request.args.get('country2')
    return jsonify(data=get_player_list(country1, country2))

@app.route('/suggest', methods = ['GET'])
def suggest():
    if request.method == "GET":
        query = request.args.get('data')
        data = suggested_players(query)
        print(data)
    return jsonify(data=data)
@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    data = {}
    if request.method == "GET":
        data["teams"] = get_team_list()
        data["roles"] = ['Wicket Keeper', 'Batsman', 'Bowler', 'All Rounder']
        data["battingroles"] = ['Opening', 'Top Order', 'Middle Order', 'Tail End']
        data["bowlingroles"] = ['Orthodox', 'Off Break', 'Leg Break', 'Googly', 'Medium', 'Fast', 'Fast Medium']
        return render_template('update.html', data=data)
    if request.method == "POST":
        name = request.get_json(force=True)["name"]
        country = request.get_json(force=True)["country"]
        playerrole = request.get_json(force=True)["playerrole"]
        battingrole = request.get_json(force=True)["battingrole"]
        bowlingrole = request.get_json(force=True)["bowlingrole"]
        update_data(name, country, playerrole, battingrole, bowlingrole)
        return jsonify(data='200')

@app.route('/stats', methods = ['GET', 'POST'])
def stats():
    if request.method == "GET":
        return render_template('stats.html')
    if request.method == "POST":
        inggBatted = request.get_json(force=True)["inggBatted"]
        notOuts = request.get_json(force=True)["notOuts"]
        runsScored = request.get_json(force=True)["runsScored"]
        ballsFaced = request.get_json(force=True)["ballsFaced"]
        fours = request.get_json(force=True)["fours"]
        sixes = request.get_json(force=True)["sixes"]
        hundreds = request.get_json(force=True)["hundreds"]
        fifties = request.get_json(force=True)["fifties"]
        highScores = request.get_json(force=True)["highScores"]
        inggBowled = request.get_json(force=True)["inggBowled"]
        ballsBowled = request.get_json(force=True)["ballsBowled"]
        runsConceded = request.get_json(force=True)["runsConceded"]
        wickets = request.get_json(force=True)["wickets"]
        maidens = request.get_json(force=True)["maidens"]
        fiveWickets = request.get_json(force=True)["fiveWickets"]
        print(fiveWickets)

@app.route('/api/countries', methods = ['GET', 'POST'])
def api_countries():
	if request.method == 'GET':
		countries = get_team_list()
		return jsonify(teams = countries)

@app.route('/api/players', methods = ['GET'])
def api_players():
	if request.method == 'GET':
		country1 = request.args.get('country1')
		country2 = request.args.get('country2')
	res = get_player_list(country1, country2)
	res = {'country_1': res[0], 'country_2': res[1]}
	return jsonify(data=res)

@app.route('/api/results', methods = ['POST'])
def api_results():
    if request.method == "POST":
        player_order = request.get_json(force=True)["playerOrder"]
        print(player_order)
        ts_win_probab, tc_win_probab, StrengthAnalysis = UI_interface_inputs.inningsPredictionValue(player_order)
        print(ts_win_probab, tc_win_probab)
        return jsonify(setting=ts_win_probab, chasing=tc_win_probab, strength=StrengthAnalysis)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
