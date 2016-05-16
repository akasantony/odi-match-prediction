# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 16:43:41 2016

@author: ABHILASH G

"""
import csv
from core.classifier.raa_player_ranking import returnbattingRAA
from core.classifier.raa_player_ranking import returnbowlingRAA
from core.classifier.player_role_dict import player_role_dict
from core.config import paths


batRAA = returnbattingRAA()

bowlRAA = returnbowlingRAA()

team_squad = []

match_table = []

final_match_prediction_vec = []

with open(paths.__VECTORS__+'team_squad.csv', 'r') as csvfile:
    
    reader = csv.DictReader(csvfile)
    count=1
    for row in reader:
        vec = []
        vec.append(row['team1']);vec.append(row['slot1']);vec.append(row['slot2']);vec.append(row['slot3']);vec.append(row['slot4'])
        vec.append(row['slot5']);vec.append(row['slot6']);vec.append(row['slot7']);vec.append(row['slot8']);vec.append(row['slot9']);vec.append(row['slot10'])
        vec.append(row['slot11']);vec.append(row['team2']);vec.append(row['slot21']);vec.append(row['slot22']);vec.append(row['slot23']);vec.append(row['slot24'])
        vec.append(row['slot25']);vec.append(row['slot26']);vec.append(row['slot27']);vec.append(row['slot28']);vec.append(row['slot29']);vec.append(row['slot30'])
        vec.append(row['slot31'])
        team_squad.append(vec)

def create_Y_axis(match_table):
    vec= []
    test_vec = []
    #print(match_table)
    for row in match_table:
        if row[1] == row[-1]:
            vec.append(1)
            test_vec.append(0)
        else:
            vec.append(0)
            test_vec.append(1)
    return vec,test_vec


with open(paths.__VECTORS__+'match.csv','r') as CSVFILE:
    reader = csv.DictReader(CSVFILE)
    for row in reader:
        vec = []
        vec.append(row['match_id']);vec.append(row['team1']);vec.append(row['team2']);vec.append(row['win_team'])
        match_table.append(vec)
    




def BattingFeatureSet(first_innings_order):
    first_batting_raa = []
    firstBattingFeatureVec = []
    topOrderBatting = 0
    topMiddleBatting = 0
    lowMiddleBatting = 0
    tailEndBatting = 0
    for row in first_innings_order:
        for c in batRAA:
            if c[0] ==int(row):
                #print(c[0])
                #print(c[1])
                first_batting_raa.append(c[1])
    #print(len(first_batting_raa))
    for i in range(0,len(first_batting_raa)):
        if i < 2:
            topOrderBatting+=first_batting_raa[i]
        if i > 1 and i < 5:
            topMiddleBatting+=first_batting_raa[i]
        if i > 4 and i < 7:
            lowMiddleBatting+=first_batting_raa[i]
        if i > 6 and i < 11:
            tailEndBatting+=first_batting_raa[i]
            
    firstBattingFeatureVec.append(round(topOrderBatting,3))
    firstBattingFeatureVec.append(round(topMiddleBatting,3))
    firstBattingFeatureVec.append(round(lowMiddleBatting,3))
    firstBattingFeatureVec.append(round(tailEndBatting,3))
    return(firstBattingFeatureVec)



def BowlingFeatureSet(first_bowling_order):
    first_bowling_raa = []
    spin_bowler = 0
    fast_bowler = 0
    count_0 = 0
    count_1 = 0
    for row in first_bowling_order:
        for c in batRAA:
            if c[0] ==int(row):   
                if c[0] in player_role_dict and player_role_dict[c[0]] == 'spin':
                    spin_bowler += c[1]
                    count_0 = count_0 + 1
                else:
                    fast_bowler += c[1]
                    count_1 = count_1 + 1
    first_bowling_raa.append(round(float(spin_bowler/count_0),3))
    first_bowling_raa.append(round(float(fast_bowler/count_1),3))
    return(first_bowling_raa)


def compareListElements(firstIngsRAAFVec,secondIngsRAAFVec):
    lis_1 = []
    lis_2 = []
    for i in range(0,len(firstIngsRAAFVec)):
        if firstIngsRAAFVec[i] > secondIngsRAAFVec[i]:
            #lis_2.append(1)
            lis_1.append(round((firstIngsRAAFVec[i]-secondIngsRAAFVec[i]),3))
            lis_2.append(round((secondIngsRAAFVec[i]-firstIngsRAAFVec[i]),3))
        else:
            #lis_2.append(0)
            lis_1.append(round((firstIngsRAAFVec[i]-secondIngsRAAFVec[i]),3))
            lis_2.append(round((secondIngsRAAFVec[i]-firstIngsRAAFVec[i]),3))
    return lis_1,lis_2
        

test_vec = []
for each in team_squad:
    firstIngsRAAFVec = []
    secondIngsRAAFVec = []
    firstIngs = []
    secIngs = []
    firstIngs.extend(each[1:12])
    #print(firstIngs)
    secIngs.extend(each[13:25])
    #print(secIngs)
    #print("\n")
    firstIngsRAAFVec = BattingFeatureSet(firstIngs)
    secondIngsRAAFVec = BattingFeatureSet(secIngs)
    firstIngsBowling = BowlingFeatureSet(secIngs)
    secondIngsBowing = BowlingFeatureSet(firstIngs)
    firstIngsRAAFVec.extend(secondIngsBowing)
    secondIngsRAAFVec.extend(firstIngsBowling)
    x,y = compareListElements(firstIngsRAAFVec,secondIngsRAAFVec)
    x.insert(0,1)
    y.insert(0,0)
    final_match_prediction_vec.append(x)
    test_vec.append(y)   
    
#print(final_match_prediction_vec)
labels = create_Y_axis(match_table)
#print(labels)

def returnMatchPredictionFeatureVector():
    return final_match_prediction_vec
    
def returnLabelsForFeatureVector():
    return labels
    
def returntestvector():
    return test_vec
    