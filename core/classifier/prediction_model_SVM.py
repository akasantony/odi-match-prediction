# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 23:27:54 2016

@author: ABHILASH G
"""
#import numpy as np
from sklearn import svm
from core.classifier.feature_vector_creation_match_prediction_by_raa import returnMatchPredictionFeatureVector
from core.classifier.feature_vector_creation_match_prediction_by_raa import returnLabelsForFeatureVector
from core.classifier.feature_vector_creation_match_prediction_by_raa import returntestvector


X = returnMatchPredictionFeatureVector()
Y = returnLabelsForFeatureVector()
C = returntestvector()
X.extend(C[3:48])
y = Y[0]
y.extend(Y[1][3:48])


neigh = svm.SVC(gamma='auto', kernel='rbf', probability=True, random_state=None, shrinking=True)
neigh.fit(X,y)


def predict_match_result(vec):
        return(neigh.predict_proba([vec]))


def predict_match_outcome_graph(vec):
    for kernel in ['linear','poly','rbf']:

        clf = svm.SVC(kernel=kernel, probability=True)

        clf.fit(X, Y[0])
        print('Kernel:'+kernel)
        print("prediction Label:",clf.predict(vec))
        print("prediction Probability:",clf.predict_proba(vec))
