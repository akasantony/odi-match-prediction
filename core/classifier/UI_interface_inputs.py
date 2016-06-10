# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 20:44:52 2016

@author: ABHILASH G
"""

from core.classifier.feature_vector_creation_match_prediction_by_raa import BattingFeatureSet
from core.classifier.feature_vector_creation_match_prediction_by_raa import BowlingFeatureSet
from core.classifier.feature_vector_creation_match_prediction_by_raa import compareListElements
from core.classifier.prediction_model_SVM import predict_match_result
from core.classifier.teamLineUp import StrengthAnalysis

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
    # TeamStructure(Vec,F_innings,S_innings)
    return(vec, F_innings, S_innings)


def inningsPredictionValue(VEC):
    ings = []
    vec1, F, S = getMatchPredictionDetails(VEC)
    VEC_ = swap_in(VEC,0,1)
    vec2, X, Y = getMatchPredictionDetails(VEC_)
    ings.append(vec1[0][1])
    ings.append(vec2[0][1])
    SA = StrengthAnalysis(F, S)
    return(round(ings[0],3),round(ings[1],3), SA)
