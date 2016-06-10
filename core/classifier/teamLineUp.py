# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:41:32 2016

@author: ABHILASH G
"""

def percentage(newNumber,originalNumber):
    increase = newNumber - originalNumber
    Percentage = (increase/originalNumber)*100
    return(round(Percentage,3))


def StrengthAnalysis(firstIngsRAAFVec,secondIngsRAAFVec):
    strengthAnalysisList = []
    for i in range(0,len(firstIngsRAAFVec)):
        if i == 0:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
        if i == 1:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
        if i == 2:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
        if i == 3:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
        if i == 4:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
        if i == 5:
            strengthAnalysisList.append(percentage(firstIngsRAAFVec[i], secondIngsRAAFVec[i]))
    return strengthAnalysisList
    print(strengthAnalysisList)

def TeamStructure(Vec, F_innings, S_innings):
    StrengthAnalysis(F_innings, S_innings)
