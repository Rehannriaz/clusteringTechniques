'''
Title: CS221-Prj-2021438-2021051-2021355-2021718
Author: Muhammad Rehan - 2021438
        Adeen Amir - 2021051
        Muhammad Arsal - 2021355
        Zaid Bin Muzammil - 2021718
Brief:  implemented a set of clustering techniques

'''


import numpy as np                                           # np used for color-coded image  
import random                                                # random used for randomizing rows while permuting
import pandas as pd                                          # used to read csv file and used for dataframe.
import cv2 as cv2                                            # cv2 used to save image of discretized
import os                                                    # used to remove temporary image
import matplotlib.pyplot as plt                              # used to save images for graphs     
import matplotlib.cm as cm                                   # used in color map
import networkx as nx                                        # used for producing graph images



def fileReader():                                            # Function to read a csv file
    # fileName = "winecsv.csv"
    fileName = "sampledataCSV.csv"
    iFile = pd.read_csv(fileName)                           # reads the file into iFile directly through pandas library

    return (iFile)




def displayColor(fileName, array, outputFileName):          # Function to display a color coded image.
    plt.imsave(fileName, np.array(array).reshape(
        len(array), len(array[0])), cmap=cm.gray)           # using PLT we are able to produce a bitmap of the discretized matrix 
                                                            

    img = cv2.imread(fileName)
    b, g, r = cv2.split(img)
    zeros_ch = np.zeros(img.shape[0:2], dtype="uint8")
                                                            # Eliminates all the other color elements except green.
    greenImg = cv2.merge([zeros_ch, g, zeros_ch])           # forms the green image
    os.remove(fileName)
    cv2.imwrite(outputFileName, greenImg)

                                                            
def PearsonCorrelation(iFile):                              # Function to find the Pearson correlation coefficient between each pair of rows in a dataset.
    corrMat = iFile

    corrMat = pd.DataFrame(corrMat.transpose())             # transposes the data.
    corrMat = corrMat.corr(method="pearson")                # applies pearson on the transposed data
    return corrMat




def discretizedMatrix(matArray):                            # Function to discretize a matrix.
    arrMean = matArray.mean()
    matArrayMean = arrMean.to_numpy()                       # calculating mean of each column.
                                                            # comparing each value with it and discretizing it accordingly.
    for i in range(len(matArray)):
        for j in range(len(matArray[i])):
            if matArray[i][j] <= matArrayMean[i]:
                matArray[j][i] = 0
                matArray[i][j] = 0
            else:
                matArray[i][j] = 1
                matArray[j][i] = 1

    for i in range(len(matArray)):
        for j in range(len(matArray[i])):
            if (matArray[i][j] == 1):
                matArray[i][j] = 0
            else:
                matArray[i][j] = 1

    plt.imsave('discretizedMatrix.png', np.array(matArray).reshape(  
        len(matArray), len(matArray[0])), cmap=cm.gray)




def colorCoded(similarityMatrix):                           # Function to display the color coded image of a discretized matrix.
    maxArr = []
    maxValue = -1

    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            if (similarityMatrix[j][i] != 1 and similarityMatrix[j][i] > maxValue):
                maxValue = similarityMatrix[j][i]

        maxArr.append(maxValue)

    for i in range(len(similarityMatrix)):                  # following steps for a colorcoded image
        for j in range(len(similarityMatrix[i])):
            similarityMatrix[j][i] = similarityMatrix[j][i]/maxArr[i]
            similarityMatrix[j][i] = similarityMatrix[j][i]*255

    displayColor('greentest.png', similarityMatrix, "GreenColorCoded1.png")



def Task1(iFile):                                           # Function to execute the Task1 of the program.
    corrMat = PearsonCorrelation(iFile)
    corrMean = corrMat.mean()
    similarityMatrix = corrMat.copy()
    discretizedMatrix(corrMat)
    colorCoded(similarityMatrix)
    print("Task 1 completed...")

    return corrMat


                                                            # Function to randomly shuffle the individual rows of the data matrix,  
def permuteMatrix(arrayDF):                                 # Takes a dataframe as a parameter.
    arrayMat = arrayDF.to_numpy()
    np.random.shuffle(arrayMat)
    print(arrayMat)
    plt.imsave('shuffle.png', np.array(arrayMat).reshape(
        len(arrayMat), len(arrayMat[0])), cmap=cm.gray)
    return (arrayMat)




def clusterRecover(permutedArray):                          # Function to recover the image clusters using Signature technique.
    sumArr = []
    meanArr = []
    MultSumArr = []
    for i in range(len(permutedArray)):                     # clusters recovered using the given steps
        sum = 0
        for j in range(len(permutedArray[i])):
            sum += permutedArray[i][j]
        sumArr.append(sum)
        meanArr.append(sumArr[i]/len(permutedArray[0]))
        MultSumArr.append(sumArr[i]*meanArr[i])

    permutedDF = pd.DataFrame(permutedArray)
    permutedDF["Signature"] = MultSumArr
                                                            # sorting on the basis of signature values.
    permutedDF = permutedDF.sort_values("Signature")
    permutedDF = permutedDF.drop(columns=["Signature"])
    return (permutedDF)




def Task2(iFile):                                           # Function to execute the Task2 of the program.
    permutedMat = permuteMatrix(iFile)                      # Takes original dataset as parameter
    permutedCorrMat = PearsonCorrelation(permutedMat)
    signaturePermutedMat = clusterRecover(permutedMat)
    Task1(signaturePermutedMat)
    print("Task 2 completed...")




def makeGraph(permutedCorrMat, GraphCounter):               # Function to create a weighted graph out of a permuted data matrix.
    sumArr = permutedCorrMat.sum()                          # sum of the weights of each edge connected to each node.
    MaxWeightofNode = sumArr.argmax()                       # Finding max weight of each node.
    DG = nx.DiGraph()                                       # Creating a weighted graph.
    DG.add_node(MaxWeightofNode)                            # add the maxWeight of Node onto the graph

    for i in range(len(permutedCorrMat)):
        if permutedCorrMat[MaxWeightofNode][i] != 0 and MaxWeightofNode != i:
            DG.add_node(i)                                  # added the neighbor nodes of maxWeight to graph 
            DG.add_edge(MaxWeightofNode, i)                 # added the edges of neighbor to maxWeight

            
            permutedCorrMat[MaxWeightofNode][i] = 0         # Setting the weight of each edge to a node zero      
            permutedCorrMat[i][MaxWeightofNode] = 0         # after recovering a cluster form it.
            for j in range(len(permutedCorrMat[i])):        # Setting the neighbors row and column to zero
                permutedCorrMat[i][j] = 0
                permutedCorrMat[j][i] = 0

    nx.draw(DG)                                             # Draw the graph
    FileName = "Graphpng\graph"+str(GraphCounter)+".png"    # Filename of the graph 
    DG.clear()                                              # clear the graph
    plt.savefig(FileName)                                   # saving each graph.
    plt.clf()                                               # clearing the plt screen
    return (permutedCorrMat)


def getThreshold(TH):                                       # used in GUI to send threshold for task 3
    Threshold = TH
    return float(Threshold)




def Task3(permutedDataSet, threshold):                     # Functtion to execute Task3, takes permutedDataSet and threshold as parameters 
    permutedCorrMat = PearsonCorrelation(permutedDataSet)
    print(permutedCorrMat)
    minimumWeight = permutedCorrMat.min()
    minimumWeight = minimumWeight.min()
    print(minimumWeight)


    if threshold < float(minimumWeight):                   # error handling if user inputs threshold out of range
        threshold = float(minimumWeight)                
    elif threshold > 1:
        threshold = 1

    print("loading...")
    for i in range(len(permutedCorrMat)):                  
        for j in range(len(permutedCorrMat[i])):
            if permutedCorrMat[i][j] < threshold:         # equates all the values below the threshold to zero
                permutedCorrMat[i][j] = 0
            if i == j:
                permutedCorrMat[i][j] = 0                 # equates diagonals to zero

    for i in range(len(permutedCorrMat)):
        sumArr = permutedCorrMat.sum()
        MaxWeightofNode = sumArr.argmax()
        if (sumArr[MaxWeightofNode] == 0):
            break
        permutedCorrMat = makeGraph(permutedCorrMat, i)  # makeGraph function repeatedly called until no more clusters are left

    print("Task 3 completed...")
