# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 16:40:31 2015

@author: Fenno
"""

import numpy as np
import sklearn.metrics as skm
import sklearn.ensemble as ske

"""
Selects some trips from a main driver, and some trips from other drivers from the feature matrix, and labels them. There is also the option to exclude trips from the main driver, to prevent duplicate picking. The labels are done such that the main driver trips are labeled as 1, and the 'fake' trips are labeled as 0.
  featurematrix: the matrix containing the features, with size (Features x Trips x Drivers)
  mainDriverID: The page of the feature matrix that contains the features of the main driver.
  numD: The number of trips from the main driver to pick
  numF: The number of trips from other drivers to pick
  alreadySelectedTrips: An array containing the trips from the main driver that have already been chosen.
output:
  features: a (numD+numF) x Features matrix containing the features of the selected trips
  labels: a (numD+numF) array containing zeros and ones, depending on what class the trip belongs to
  chosentrips: the chosen trips, equal to the input, concatenated with the trips chosen in this function.
"""

def getTrips(featureMatrix, mainDriverId, numReal = 200, numFake=200):
    numFea, numTri, numDri = np.shape(featureMatrix)
    mainTrips = np.transpose(featureMatrix[:,:,mainDriverId])
    mainTrips = mainTrips[:numReal, :]
    randi = np.random.randint(numTri, size = (numFake, 1))
    randj = np.random.randint(numDri, size = (numFake, 1)) 
    randj[randj==mainDriverId] = (randj[randj==mainDriverId] + 1)%numDri
    fakeTrips = np.array([featureMatrix[:, randi[i], randj[i]] for i in range(numFake)]) 
    fakeTrips = np.reshape(fakeTrips, (numFake, numFea)) 
    return np.vstack((mainTrips, fakeTrips)), np.concatenate((np.ones(numReal), np.zeros(numFake)))
    

"""
Evaluates a given probability array with 'gold' standard labels and a threshold
As output, gives precision and recall of both classes.
probabilities: an array containing the probability that the trip belongs to class 1
labels: the actual label of the trip
threshold: how high the probability needs to be for the trip to be considered a part of class 1
"""
def evaluation(probabilities, labels, threshold):
    probabilities = (probabilities >= threshold).astype(int)
    precision = skm.precision_score(labels, probabilities, average=None) 
    recall = skm.recall_score(labels, probabilities, average=None)
    return precision, recall

"""
Trains a model using logistic regression, given some features, and their true class.
features: a list of trip features, in a (trips x features) size
labels: the true labels of the given trips, in array form
penalty, dual, tol, C, class_weight: argument for the logistic regression classifier
see sk_learn documentation for info on what they do
"""
def trainModel(features, labels, criterion = 'gini', max_features = 'auto', n_trees = 10, sample_weight = None, n_jobs = 1):
   model = ske.RandomForestClassifier(n_estimators = n_trees, criterion = criterion, max_features = max_features, n_jobs = n_jobs)
   return model.fit(features, labels, sample_weight = sample_weight)

"""
Given a model trained with the trainModel function, and some features, gives an array with the probabilities those features belong to class 1 (aka are real trips)   
"""
def predictClass(model, features):
    return model.predict_proba(features)[:,1]    

def printMatlabStyle(threedmatrix):
    for i in range(np.shape(threedmatrix)[2]):
        print 'matrix[:,:,' + `i` + '] = '
        print threedmatrix[:,:,i]

# Example of the above functions, the input is a feature matrix, output is a trained model and feedback on it classfying something
if __name__ == "__main__":
    featureMatrix = np.array([[[4,2,3], [4,1,2],[6,2,1], [4,1,2]], [[2,3,1],[6,3,1],[4,1,1],[8,8,8]]])
    numF, numT, numD = np.shape(featureMatrix)
    print((numF, numT, numD))
    #trainTrips, trainLabels, chosen = getTrips(featureMatrix, 0, 2, 5)
    #model = trainModel(trainTrips, trainLabels)
    #testTrips, testLabels, _ = getTrips(featureMatrix, 0, 1, 1, chosen)
    #predictions = predictClass(model, testTrips)
    #print evaluation(predictions, testLabels, 0.5)
    printMatlabStyle(featureMatrix)
    print(getTrips(featureMatrix, 0, numT, numT))