# -*- coding:UTF-8 -*-
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import random
import types

def loadDataSet(fileName):
    samples2D = []; 
    labels = []
    dataFileTxt = open(fileName)
    for line in dataFileTxt.readlines():
        termsOfLine = line.strip().split('\t')
        samples2D.append([float(termsOfLine[0]), float(termsOfLine[1])])
        labels.append(float(termsOfLine[2]))
    return samples2D,labels


class SMOSolver(object):
    
    def __init__(self, samples2D, labels):
        self.samplesMat = np.mat(samples2D)
        self.labelsColumn = np.mat(labels).transpose()
        self.sampleNum, self.sampleDimension = np.shape(self.samplesMat)
        self.alphasColumn = np.mat(np.zeros((self.sampleNum,1)))
        self.b = 0
        
    """
    函数说明:简化版SMO算法

    Parameters:
        C - 惩罚参数
        toler - 松弛变量
        maxIter - 最大迭代次数
    
    针对不符合KKT条件(设定一定的容错率)的alpha的优化
    在设定的迭代最大周期中保持alpha变量不变,才能退出循环
    """
    def smoSimple(self, C, toler = 0.001, maxIter = 50):
        iterNum = 0
        self.C = C
        while (iterNum < maxIter):
            self.alphaPairChangedNum = 0
            print("第%d次迭代"  %(iterNum+1))
            for AlphaindexI in range(self.sampleNum):
                if (self.AlphaIndexNotFitKKTconditon(AlphaindexI, toler)):
                    AlphaindexJ = self.selectAnotherAlphaIndexExcept(AlphaindexI)
                    self.updateAlphaPairAndB(AlphaindexI, AlphaindexJ)
                    print("\t违反KKT条件样本:%d, alpha优化次数:%d" %(AlphaindexI,self.alphaPairChangedNum))
            iterNum = self.updateIterNumByalphaPairChanged(iterNum)
        return self.b, self.alphasColumn

    def getPredictError(self, sampleindex):
         Ei = self.predict(self.getSamplebyIndex(sampleindex))- float(self.labelsColumn[sampleindex])
         return Ei
   
    def predict(self, sampleRow):
#         y = wx + b
         fXi = float(self.getW() * sampleRow.T) + self.b
         return fXi

    def getW(self):
        # return [[0.8, -0.28]]
        wRow = np.multiply(self.alphasColumn,self.labelsColumn).T*self.samplesMat
        return wRow
    
    def getSamplebyIndex(self, index):
        sampleRow = self.samplesMat[index,:]
        return sampleRow
       
    """
    toler为容错限度,在toler范围内违反KKT条件是允许的
    """
    def AlphaIndexNotFitKKTconditon(self, index, toler):
        self.Ei = self.getPredictError(index)
        #condition1 = (self.labelsColumn[index] * self.Ei < -toler) and (self.alphasColumn[index] < self.C)
        #condition2 = (self.labelsColumn[index] * self.Ei > toler) and (self.alphasColumn[index] > 0)
        condition1 = (self.alphasColumn[index] == 0) and (self.labelsColumn[index]*self.Ei<-toler)
        condition2 = (0 <self.alphasColumn[index] < self.C) and \
            ((self.labelsColumn[index]*self.Ei <- toler) or (self.labelsColumn[index]*self.Ei > toler))
        condition3 = (self.alphasColumn[index] == self.C) and (self.labelsColumn[index]*self.Ei > toler)
        return condition1 or condition2 or condition3
        
    def selectAnotherAlphaIndexExcept(self, AlphaIndex):
        another = AlphaIndex            #选择一个不等于AlphaIndex的alphaindex
        while (another == AlphaIndex):
            another = int(random.uniform(0, self.sampleNum))
        return another
    
    def updateAlphaPairAndB(self, i, j, precision = 1e-5):
        self.alphaIold = self.CopyOldAlpha(i)
        self.alphaJold = self.CopyOldAlpha(j)
        if(self.IsSkip(i, j) == 0):
            self.updateAlphaJ(i, j)
            if (abs(self.alphasColumn[j] - self.alphaJold) > precision): 
                self.updateAlphaI(i, j)
                self.alphaPairChangedNum += 1
                self.updateB(i, j)
            else:
                print("\tupdateAlphaPairAndB:alpha_j变化太小"); 
    
    def CopyOldAlpha(self, index):
        return self.alphasColumn[index].copy(); 
   
    """
    为加速迭代,一些不需要继续计算的场合
    """
    def IsSkip(self, i, j):
        self.eta = self.CalculateEta(i, j)
        """
        if self.eta >= 0: 
            print("\tIsSkip:eta>=0");
            return 1
        """
        self.H, self.L = self.CalculateAlphaJUpandDown(i, j, self.C)
        if self.H == self.L:
            print("\tIsSkip:L==H");
            return 1
        return 0

    def CalculateEta(self, i, j):
        eta = 2.0 * self.Cross(i, j) - self.Cross(i, i) - self.Cross(j, j)
        return eta

    def Cross(self, xRowIndex1, xRowIndex2):
        return self.samplesMat[xRowIndex1,:] * self.samplesMat[xRowIndex2,:].T
    
    def CalculateAlphaJUpandDown(self, i, j, C):
        if (self.labelsColumn[i] != self.labelsColumn[j]):
            L = max(0, self.alphasColumn[j] - self.alphasColumn[i])
            H = min(C, C + self.alphasColumn[j] - self.alphasColumn[i])
        else:
            L = max(0, self.alphasColumn[j] + self.alphasColumn[i] - C)
            H = min(C, self.alphasColumn[j] + self.alphasColumn[i])
        return H, L

    def updateAlphaJ(self, i, j):
        self.Ej = self.getPredictError(j)
        self.alphasColumn[j] -= self.labelsColumn[j]*(self.Ei - self.Ej)/self.eta
        self.alphasColumn[j] = self.clipAlpha(self.alphasColumn[j], self.H, self.L)

    """
    函数说明:修剪alpha
    """
    def clipAlpha(self,alpha,high,low):
        if alpha > high:
            alpha = high
        if alpha < low:
            alpha = low
        return alpha

    def updateAlphaI(self, i, j):
        self.alphasColumn[i] += self.labelsColumn[j]*self.labelsColumn[i]*(self.alphaJold - self.alphasColumn[j])

    def updateB(self, i, j):
        b1 = self.b - self.Ei \
            - self.labelsColumn[i]*(self.alphasColumn[i]-self.alphaIold)*self.Cross(i, i) \
            - self.labelsColumn[j]*(self.alphasColumn[j]-self.alphaJold)*self.Cross(i, j)
        b2 = self.b - self.Ej \
            - self.labelsColumn[i]*(self.alphasColumn[i]-self.alphaIold)*self.Cross(i, j) \
            - self.labelsColumn[j]*(self.alphasColumn[j]-self.alphaJold)*self.Cross(j, j)
        
        if (0 < self.alphasColumn[i] < self.C): 
            self.b = b1
        elif (0 < self.alphasColumn[j] < self.C): 
            self.b = b2    
        else: 
            self.b = (b1 + b2)/2.0 
   
    """
    在设定的迭代最大周期中保持alpha变量不变,才能退出循环
    """
    def updateIterNumByalphaPairChanged(self, iterNum): 
        if (self.alphaPairChangedNum == 0): 
            return iterNum + 1
        else: 
            return 0
    """
    Parameters:
        samples2D - 数据矩阵
        w - 直线法向量
    """
    def showClassifer(self,samples2D):
        #绘制样本点
        data_plus = []                                  #正样本
        data_minus = []                                 #负样本
        for i in range(len(self.samplesMat)):
            if self.labelsColumn[i] > 0:
                data_plus.append(self.samplesMat[i])
            else:
                data_minus.append(self.samplesMat[i])
        data_plus_np = np.array(data_plus)              #转换为numpy矩阵
        data_minus_np = np.array(data_minus)            #转换为numpy矩阵
        plt.scatter(np.transpose(data_plus_np)[0], np.transpose(data_plus_np)[1], s=30, alpha=0.7)   #正样本散点图
        plt.scatter(np.transpose(data_minus_np)[0], np.transpose(data_minus_np)[1], s=30, alpha=0.7) #负样本散点图
        #绘制直线,self.b = [[3.5]],w = [[1,2]]
        w = self.getW()
        b = float(self.b)
        x1 = max(samples2D)[0]
        x2 = min(samples2D)[0]
        a1 = float(w[0,0])
        a2 = float(w[0,1])
        print(a1,a2,x1,x2)
        y1, y2 = (-b- a1*x1)/a2, (-b - a1*x2)/a2
        print(y1,y2)
        plt.plot([x1, x2], [y1, y2])
        y1, y2 = (-b+1- a1*x1)/a2, (-b+1 - a1*x2)/a2
        plt.plot([x1, x2], [y1, y2])
        y1, y2 = (-b-1- a1*x1)/a2, (-b-1 - a1*x2)/a2
        plt.plot([x1, x2], [y1, y2])
        
        
        #找出支持向量点
        for i, alpha in enumerate(self.alphasColumn):
            if alpha > 0:
                x, y = samples2D[i]
                plt.scatter([x], [y], s=150, c='none', alpha=0.7, linewidth=1.5, edgecolor='red')
        plt.show()

if __name__ == '__main__':
    samples2D, labels = loadDataSet('testDataSimple.txt')
    smo = SMOSolver(samples2D, labels)
    b,alphasColumn = smo.smoSimple(C = 0.6, toler = 0.001, maxIter = 10)
    print(alphasColumn)
    smo.showClassifer(samples2D)
    print("w=",smo.getW(),"b=",b)

