###############3
#
# This code has been taken from the followinglink and modified as per the reqirement. 
#http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
#
#
#
#

import csv
import random
import math
import operator



def euclideandistance(inst1, inst2, length):
    """Calculate Eculidean distance between two samples.  """
    distance = 0
    for x in range(length):
        distance+= pow((float(inst1[x])-float(inst2[x])),2)
    return math.sqrt(distance)


def getNeighbour(trainingSet, testInstance, k):
    """ This will find k most nearest neighbor from the trainingSet for a given testInstance. """
    distances = []
    length = len(testInstance)
    #print(length)
    for x in range(len(trainingSet)):
        dist= euclideandistance(testInstance,trainingSet[x], length )
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getNeighbourTest(trainingSet, testInstance, k):
    """ Repetition of above function. It is used by ibktest() function.  """
    distances = []
    length = len(testInstance)-1
    #print(length)
    for x in range(len(trainingSet)):
        dist= euclideandistance(testInstance,trainingSet[x], length )
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    """ This method will predict if executable is packed or not packed on the basis of neighbors  """
    classVotes = {}
    response = '' 
    for x in range(len(neighbors)):
        response= neighbors[x][-1]
        if response in classVotes:
            classVotes[response] +=1
        else:
            classVotes[response] =1
        sortedVoted = sorted(classVotes.items(), key=operator.itemgetter(1), reverse =True)
        return(sortedVoted[0][0])


def getAccuracy(testSet, predictions):
    """ This method will check accurcy of the prediction. It is used by ibktest() method.  """ 
    correct=0
    #print(predictions)
    for x in range (len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct= correct+1
    #print("sdff----",correct)
    return (correct/float(len(testSet)))*100.0


def ibk(TestingList):
    """This method is called by skEntropy.py to determine if executable is packed or not. """
    csvfile = open("sample/data.csv", "r")
    lines = csv.reader(csvfile)
    dataset = list(lines)
    dataset = dataset[1:]
    """K is sleceted randomly. I am taking 10% of totol sample data.""" 
    k=int(len(dataset)*.1)
    neighbours = getNeighbour(dataset,TestingList,k)
    #print(neighbours)
    result = getResponse(neighbours)
    return result


def ibktest():
    """ This mehod  can use to test the accuracy of data(sample/data.csv) in correctly classifying packed and not packed executable. The accuracy is more than 98%. """
    csvfile = open("sample/data.csv", "r")
    lines = csv.reader(csvfile)
    dataset = list(lines)
    dataset = dataset[1:]
    trainingset = []
    testingset = []
    perValue = 0.90
    for x in range(len(dataset)):
        for y in range(4):
            dataset[x][y]= (dataset[x][y])
        if random.random() < perValue:
            trainingset.append(dataset[x])
        else:
            testingset.append(dataset[x])
    predictions = []
    k=10

    for x in range (len(testingset)):
        neighbours = getNeighbourTest(trainingset,testingset[x],k)
        #print(neighbours)
        result = getResponse(neighbours)
        predictions.append(result)
        """Uncomment the below line if you want to check predicted result and actual result """
        #print('> predicted=' + repr(result) + ', actual=' + repr(testingset[x][-1]))
    accuracy1 = getAccuracy(testingset,predictions)
    print('Accuracy: ' + repr(accuracy1) + '%')
