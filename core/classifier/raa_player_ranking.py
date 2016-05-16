# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 00:03:24 2016

@author: ABHILASH G
"""
import csv
from operator import itemgetter
from core.classifier.tournament_query import returnAvgBPerformanceVec
from core.classifier.tournament_query import returnAvgBWPerformanceVec
from core.config import paths

batFeatureVec = []
bowlerFeatureVec = []

with open(paths.__VECTORS__+'raaPlayer.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bvec = []
        bwvec = []
        bvec.append(row['player_id']);bvec.append(row['NumOfInningsBatted']);bvec.append(row['NotOutInnings']);
        bvec.append(row['runs_scored']);bvec.append(row['balls_faced']);bvec.append(row['Bat_AVG']);
        bvec.append(row['Bat_SR']);bvec.append(row['MRA']);bvec.append(row['BRPI']);bvec.append(row['HS']);
        if bvec[1:] != bvec[:-1]:
            for i in range(0,5):
                bvec[i] = int(bvec[i])
            for i in range(5,9):
                bvec[i] = float(bvec[i])
            bvec[-1] = int(bvec[-1])
            batFeatureVec.append(bvec)
        ####Bowling Card
        bwvec.append(row['player_id']);bwvec.append(row['NumOfIngsBowled']);bwvec.append(row['balls_bowled']);
        bwvec.append(row['runs_conceded']);bwvec.append(row['WCKTS']);bwvec.append(row['BW_AVG']);
        bwvec.append(row['BW_SR']);bwvec.append(row['BW_ECN']);bwvec.append(row['MDO']);
        if bwvec[1:] != bwvec[:-1] and bwvec[1] != '0':
            for i in range(0,5):
                bwvec[i] = int(bwvec[i])
            for i in range(5,8):
                bwvec[i] = float(bwvec[i])
            bwvec[-1] = int(bwvec[-1])
            bowlerFeatureVec.append(bwvec)
        
avgODIBatsman = returnAvgBPerformanceVec()
avgODIBowler = returnAvgBWPerformanceVec()				


def battingRAA(batFeatureVec,AvgBVec):
    #print("\n\nBatting Rankings:\n\n")
    batting_RAA = []
    for row in batFeatureVec:
        vec=[]
        if row[4]== 0:
            B_RAA = ((float(row[3]))-(float(AvgBVec[1])*float(row[4]))+float(AvgBVec[0])*float(row[4])*(float(AvgBVec[2])-float(0)))
        else:
            B_RAA = ((float(row[3]))-(float(AvgBVec[1])*float(row[4]))+float(AvgBVec[0])*float(row[4])*(float(AvgBVec[2])-float((row[1]-row[2])/row[4])))
            vec.append(row[0])            
            vec.append(round((B_RAA/(10*27.341)),3))
            batting_RAA.append(vec) 
    return(sorted(batting_RAA, key=itemgetter(-1), reverse=True))

#print(battingRAA(batFeatureVec,avgODIBatsman))


def bowlingRAA(bowlerFeatureVec,avgBWVec):
    #print("\n\nBowling Rankings:\n\n")
    bowling_RAA = []
    for eachEntry in bowlerFeatureVec:
        vec = []
        if eachEntry[1] != 0:        
            BW_RAA_2 = round(((float(avgBWVec[1])*float(eachEntry[2]))-float(eachEntry[3])),3) + (float(avgBWVec[0])*float(eachEntry[2]))*float(round((eachEntry[4]/eachEntry[2]),3) - float(avgBWVec[-1]))
            BW_RAA = round(BW_RAA_2/round(float(10*avgBWVec[0]),3),3)
            vec.append(eachEntry[0])
            vec.append(BW_RAA)
            bowling_RAA.append(vec)
    return(sorted(bowling_RAA, key=itemgetter(-1), reverse=True))
         

def returnTopBatsman():
    list1 =  battingRAA(batFeatureVec,avgODIBatsman)
    list_ = list1[0:10]
    return(list_)      
    
def returnTopBowlers():
    list2 = bowlingRAA(bowlerFeatureVec,avgODIBowler)
    list_ = list2[0:10]
    return(list_)
    
def returnbattingRAA():
    list_ =  battingRAA(batFeatureVec,avgODIBatsman)
    return list_
    
def returnbowlingRAA():
    list_  = bowlingRAA(bowlerFeatureVec,avgODIBowler)
    return list_
#print(bowlingRAA(bowlerFeatureVec,avgODIBowler))
