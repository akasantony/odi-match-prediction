# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:21:02 2016

@author: ABHILASH G
"""
from core.classifier.tournament_query import returnAvgBPerformanceVec
from core.classifier.tournament_query import returnAvgBWPerformanceVec

def getData(Player_id):
    vec = []
    print("Enter Batting Statistics......!!!\n")
    runs = float(input("Enter Runs Scored:"))
    balls_faced = float(input("Enter Balls Faced:"))
    NoOuts = float(input("Enter Number Innings Got Out:"))
    print("\nEnter Bowling Statistics......!!!\n")
    runs_conceded = float(input("Enter Runs Conceded As Bowler:"))
    balls_bowled = float(input("Enter Numnber of balls bowled:"))
    wickets_taken = float(input("Enter Number of wickets taken:\n"))

    vec.append(Player_id);vec.append(runs);vec.append(balls_faced);vec.append(NoOuts);vec.append(round((NoOuts/balls_faced),3));vec.append(runs/NoOuts);vec.append(runs_conceded);vec.append(balls_bowled);vec.append(wickets_taken);vec.append(round((runs/wickets_taken),3));vec.append(round((wickets_taken/balls_bowled),3));
    return vec

data = getData(1226)
print(data)
