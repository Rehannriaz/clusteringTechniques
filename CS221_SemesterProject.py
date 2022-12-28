import csv
import numpy as np
import random
import pandas as pd
import cv2 as cv2
import scipy.stats as stats
import io
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image, ImageChops
import networkx as nx


def fileReader():
    fileName = "sampledataCSV.csv"
    iFile = pd.read_csv(fileName)

    return (iFile)


def displayColor(fileName, array, outputFileName):
    plt.imsave(fileName, np.array(array).reshape(
        len(array), len(array[0])), cmap=cm.gray)

    img = cv2.imread(fileName)
    b, g, r = cv2.split(img)
    zeros_ch = np.zeros(img.shape[0:2], dtype="uint8")
    greenImg = cv2.merge([zeros_ch, g, zeros_ch])
    os.remove(fileName)
    cv2.imwrite(outputFileName, greenImg)


def PearsonCorrelation(iFile):
    corrMat = iFile

    corrMat = pd.DataFrame(corrMat.transpose())
    corrMat = corrMat.corr(method="pearson")
    return corrMat


def discretizedMatrix(matArray):
    arrMean = matArray.mean()
    matArrayMean = arrMean.to_numpy()
    for i in range(len(matArray)):
        for j in range(len(matArray[i])):
            if matArray[i][j] <= matArrayMean[i]:   # PROBLEM HERE
                matArray[j][i] = 0
                matArray[i][j] = 0
            else:
                matArray[i][j] = 1
                matArray[j][i] = 1

    for i in range(len(matArray)):                   # # removable if problem fixed
        for j in range(len(matArray[i])):
            if (matArray[i][j] == 1):
                matArray[i][j] = 0
            else:
                matArray[i][j] = 1

    plt.imsave('discretizedMatrix.png', np.array(matArray).reshape(
        len(matArray), len(matArray[0])), cmap=cm.gray)


def colorCoded(similarityMatrix):
    maxArr = []
    maxValue = -1

    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            if (similarityMatrix[j][i] != 1 and similarityMatrix[j][i] > maxValue):
                maxValue = similarityMatrix[j][i]

        maxArr.append(maxValue)

    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            similarityMatrix[j][i] = similarityMatrix[j][i]/maxArr[i]
            similarityMatrix[j][i] = similarityMatrix[j][i]*255

    displayColor('greentest.png', similarityMatrix, "GreenColorCoded1.png")


def Task1(iFile):
    corrMat = PearsonCorrelation(iFile)
    corrMean = corrMat.mean()
    similarityMatrix = corrMat.copy()
    discretizedMatrix(corrMat)
    colorCoded(similarityMatrix)

    return corrMat


def clusterRecover(permutedArray):
    sumArr = []
    meanArr = []
    MultSumArr = []
    for i in range(len(permutedArray)):
        sum = 0
        for j in range(len(permutedArray[i])):
            sum += permutedArray[i][j]
        sumArr.append(sum)
        meanArr.append(sumArr[i]/len(permutedArray[0]))
        MultSumArr.append(sumArr[i]*meanArr[i])

    permutedDF = pd.DataFrame(permutedArray)
    permutedDF["Signature"] = MultSumArr
    permutedDF = permutedDF.sort_values("Signature")
    permutedDF = permutedDF.drop(columns=["Signature"])
    return (permutedDF)


def Task2(iFile):
    permutedMat = permuteMatrix(iFile)
    permutedCorrMat = PearsonCorrelation(permutedMat)
    signaturePermutedMat = clusterRecover(permutedMat)
    Task1(signaturePermutedMat)
    # return (permutedMat)


def permuteMatrix(arrayDF):
    arrayMat = arrayDF.to_numpy()
    np.random.shuffle(arrayMat)
    print(arrayMat)
    plt.imsave('shuffle.png', np.array(arrayMat).reshape(
        len(arrayMat), len(arrayMat[0])), cmap=cm.gray)
    return (arrayMat)

def makeGraph(permutedCorrMat, GraphCounter):
    sumArr = permutedCorrMat.sum()
    MaxWeightofNode = sumArr.argmax()

    DG = nx.DiGraph()
    DG.add_node(MaxWeightofNode)

    for i in range(len(permutedCorrMat)):
        if permutedCorrMat[MaxWeightofNode][i] != 0 and MaxWeightofNode != i:
            DG.add_node(i)
            DG.add_edge(MaxWeightofNode, i)
            
            permutedCorrMat[MaxWeightofNode][i] = 0
            permutedCorrMat[i][MaxWeightofNode] = 0
            for j in range(len(permutedCorrMat[i])):
                permutedCorrMat[i][j] = 0
                permutedCorrMat[j][i] = 0

    nx.draw(DG)
    FileName = "Graphpng\graph"+str(GraphCounter)+".png"
    DG.clear()
    plt.savefig(FileName)
    plt.clf()
    return (permutedCorrMat)


def getThreshold(TH):
    Threshold=TH
    return float(Threshold)


def Task3(permutedDataSet,threshold):
    permutedCorrMat = PearsonCorrelation(permutedDataSet)
    print(permutedCorrMat)
    minimumWeight = permutedCorrMat.min()
    minimumWeight = minimumWeight.min()

    print(minimumWeight)
    # threshold = float(input("Enter a threshold,Minimum Value is " +
    #                   str(minimumWeight)+", and Max of 1: "))

    if threshold < float(minimumWeight):
        threshold = float(minimumWeight)
    elif threshold > 1:
        threshold = 1
    print("workss")

    for i in range(len(permutedCorrMat)):
        for j in range(len(permutedCorrMat[i])):
            if permutedCorrMat[i][j] < threshold:
                permutedCorrMat[i][j] = 0
            if i == j:
                permutedCorrMat[i][j] = 0

    k = 0
    for i in range(len(permutedCorrMat)):
        sumArr = permutedCorrMat.sum()
        MaxWeightofNode = sumArr.argmax()
        if (sumArr[MaxWeightofNode] == 0):
            break
        permutedCorrMat = makeGraph(permutedCorrMat, i)
        

    print("done")

# def main():
#     Task1(fileReader())
#     # Task2(fileReader())
#     # Task3(permuteMatrix(fileReader()))



# main()
