import numpy as np
import pandas as pd
import operator
import csv
trainfilename = '/Users/huihui/PycharmProjects/machinelearninginaction/Ch02/train.csv'
testfilename = '/Users/huihui/PycharmProjects/machinelearninginaction/Ch02/test.csv'
def load_trainDataSet(filename):
    l = []
    with open(filename) as file:
        lines =  csv.reader(file)
        for line in lines:
            l.append(line)

    l = l[1:-1]
    l = np.array(l)
    labels = l[:,0]
    trainDataSet = l[:,1:]
    trainDataSet = trainDataSet.astype(int)#将string 转化为 整数

    '''
    将非0得像素值转为1，只留下二值，便于计算
    '''
    trainDataSet = nomalizing(trainDataSet)
    #ss = trainDataSet

    return trainDataSet,labels



def nomalizing(array):
    m,n = np.shape(array)
    for i in range(m):
        for j in range(n):
            if array[i][j] != 0:
                array[i][j] = 1

    return array




def load_testDataSet(testfilename):
    l = []
    with open(testfilename) as file:
        lines = csv.reader(file)
        for line in lines:
            l.append(line)

    l = l[1:-1]
    l = np.array(l)
    #labels = l[:, 0]
    testDataSet = l
    testDataSet = testDataSet.astype(int)  # 将string 转化为 整数

    '''
    将非0得像素值转为1，只留下二值，便于计算
    '''
    testDataSet = nomalizing(testDataSet)

    return testDataSet

#res = load_trainDataSet(trainfilename)
#print(res)

#testdata = load_testDataSet(testfilename)
#print(testdata)

def classify0(inX,dataSet,labels,k):
    '''

    :param inX: the input vector to classify待分类
    :param dataSet:our full matrix of training examples训练样本
    :param labels:a vector of labels
    :param k:he number of nearest neighbors to use in the voting.
    :return:
    '''
    #inX = np.mat(inX)
    #dataSet = np.mat(dataSet)

    dataSetSize = dataSet.shape[0]#行数
    #np.tile()用于扩充数组元素,下面将inX扩充为与训练样本一样的行数x1列的一个矩阵
    diffMat = np.tile(inX,(dataSetSize,1)) - dataSet
    sqdiffMat = diffMat ** 2
    sqDistances = sqdiffMat.sum(axis=1)#坐标轴x,横向相加（x^2+y^2）
    distance = sqDistances ** 0.5
    sortedDistIndicies = distance.argsort()#数组值从小到大的索引值，并非移动元素大小排序
    s= sortedDistIndicies[0]
    ss = sortedDistIndicies[1]
    classCount = {}
    #dsfd
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]#labels[0]='A'
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]

def saveResult(result):
    with open('result.csv','w') as myFile:
        myWriter = csv.writer(myFile)
        for i in result:
            tmp = []
            tmp.append(i)
            myWriter.writerow(tmp)


def handwriterClassTest():
    trainDataSet,trainLabes = load_trainDataSet(trainfilename)
    testDataSet = load_testDataSet(testfilename)
    m,n = np.shape(testDataSet)
    erroeNum = 0
    resultList = []

    for i in range(m):
        classifierResult = classify0(testDataSet[i],trainDataSet,trainLabes,5)
        resultList.append(classifierResult)

        print('the classifier came back with : %d',(classifierResult))

    saveResult(resultList)


handwriterClassTest()