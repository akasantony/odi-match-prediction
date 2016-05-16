# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 22:53:34 2016

@author: ABHILASH G
"""

import pymysql

conn = pymysql.connect("localhost","root","root","cricketcommentaryanalysis")

cursor1 = conn.cursor()
cursor2 = conn.cursor()
bow_cursor=conn.cursor()

query1 = """select sum(runs) as total_runs,sum(balls_faced) as balls_bowled,count(bowler)
from batting_card"""

query2 = """SELECT sum(numofMatchesNotOut) as NOI FROM notout"""

query3 = """select sum(balls_bowled),sum(runs_conceded),sum(wickets) from bowling_card"""

Tournament_Batting_Performance=[]
Tournament_Bowling_Performance=[]
averageBatsmanCWC = []
averageBowlerCWC = []

try:
    cursor1.execute(query1)
    cursor2.execute(query2)
    bow_cursor.execute(query3)
    bowling_results=bow_cursor.fetchone()
    results2 = cursor2.fetchone()
    NOI = results2[0]
    results1 = cursor1.fetchall()
    for row_ in results1:
        Tot_Runs_tournament=row_[0]
        Tot_Balls_Tournament=row_[1]
        Tot_players_batted=row_[2]
        NWCT=Tot_players_batted-NOI
        Tournament_Batting_Performance.append(Tot_Runs_tournament)
        Tournament_Batting_Performance.append(Tot_Balls_Tournament)
        Tournament_Batting_Performance.append(NWCT)
    
    Tournament_Bowling_Performance.append(bowling_results[0])
    Tournament_Bowling_Performance.append(bowling_results[1])
    Tournament_Bowling_Performance.append(bowling_results[2])
    
except:
    print("Error: Unable to Fetch Data")

def overallBattingPerformance(PerformanceVec):
    #print("Batting Statistics....\n")
    
    overallBattingAverage = round((PerformanceVec[0]/PerformanceVec[2]),3)
    overallBattingStrikeRate = round((PerformanceVec[0]/PerformanceVec[1]),3)
    AverageOutRate = round((PerformanceVec[2]/PerformanceVec[1]),3)
    averageBatsmanCWC.append(overallBattingAverage)
    averageBatsmanCWC.append(overallBattingStrikeRate)
    averageBatsmanCWC.append(AverageOutRate)
    #print(overallBattingAverage)
    #print(overallBattingStrikeRate)
    #print(AverageOutRate)
    
    
    
def overallBowlingPerformance(PerformanceVec):
    #print("\nBowling Statistics...\n")
    
    overallBowlingAverage = round((PerformanceVec[1]/PerformanceVec[-1]),3)
    AverageRunsPerBall = round((PerformanceVec[1]/PerformanceVec[0]),3)
    overallAverageWicketsPerBall = round((PerformanceVec[-1]/PerformanceVec[0]),3)
    averageBowlerCWC.append(overallBowlingAverage)
    averageBowlerCWC.append(AverageRunsPerBall)
    averageBowlerCWC.append(overallAverageWicketsPerBall)
    
    #print(overallBowlingAverage)
    #print(AverageRunsPerBall)
    #print(overallAverageWicketsPerBall)    
        
def returnAvgBPerformanceVec():
    overallBattingPerformance(Tournament_Batting_Performance)
    return averageBatsmanCWC
    
def returnAvgBWPerformanceVec():
    overallBowlingPerformance(Tournament_Bowling_Performance)
    return averageBowlerCWC
    

#bat_list=overallBattingPerformance(Tournament_Batting_Performance)
#bow_list=overallBowlingPerformance(Tournament_Bowling_Performance)

#print(bat_list)
#print(bow_list)