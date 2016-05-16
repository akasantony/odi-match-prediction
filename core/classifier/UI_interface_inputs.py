# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 20:44:52 2016

@author: ABHILASH G
"""

from core.classifier.feature_vector_creation_match_prediction_by_raa import BattingFeatureSet
from core.classifier.feature_vector_creation_match_prediction_by_raa import BowlingFeatureSet
from core.classifier.feature_vector_creation_match_prediction_by_raa import compareListElements
from core.classifier.prediction_model_SVM import predict_match_result
from core.classifier.teamLineUp import TeamStructure

def swap_in(lst, fro, to):
    lst[fro], lst[to] = lst[to], lst[fro]
    return lst
    

def getMatchPredictionDetails(Vec):
    F_innings = []
    S_innings = []
    F_innings = BattingFeatureSet(Vec[0])
    S_bowling = BowlingFeatureSet(Vec[0])
    S_innings = BattingFeatureSet(Vec[1])
    F_bowling = BowlingFeatureSet(Vec[1])
    F_innings.extend(S_bowling)
    S_innings.extend(F_bowling)
    X,Y = compareListElements(F_innings, S_innings)
    X.insert(0,1)
    Y.insert(0,0)
    vec = predict_match_result(X)
    TeamStructure(Vec,F_innings,S_innings)
    return(vec)
    

def inningsPredictionValue(VEC):
    ings = []
    # VEC = [['502', '514', '505', '508', '501', '515', '512', '506', '507', '510', '513'],['1215', '1203', '1201', '1202', '1213', '1207', '1208', '1212', '1209', '1206', '1211']]
    vec1 = getMatchPredictionDetails(VEC)
    VEC_ = swap_in(VEC,0,1)
    vec2 = getMatchPredictionDetails(VEC_)
    ings.append(vec1[0][1])
    ings.append(vec2[0][1])
    return(round(ings[0],3),round(ings[1],3))


    
# f,s = inningsPredictionValue()
# print("Batting First Winning %:",f)
# print("Second Batting Winning %:",s)