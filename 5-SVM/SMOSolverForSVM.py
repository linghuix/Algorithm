# -*- coding:UTF-8 -*-
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import random
import types
import simpleSMOSolver as my

class SMOSolver(my.simpleSMOSolver):
    
    def __init__(self, samples2D=[], labels=[]):
        self.samplesMat = np.mat(samples2D)
        self.labelsColumn = np.mat(labels).transpose()
        self.sampleNum, self.sampleDimension = np.shape(self.samplesMat)
        self.alphasColumn = np.mat(np.zeros((self.sampleNum,1)))
        self.alphasNotBound = np.zeros((self.sampleNum, 1))
        self.E  = np.zeros((self.sampleNum, 1))
        self.MaxEiandIndex = [0,0]
        self.b = 0
        self.IsAlphaUpdate = 0;
        
        self.alphaPairChangedNum = 1
        
    """
    Parameters:
        C - 惩罚参数
        toler - 松弛变量
        maxIter - 最大迭代次数
    
    针对不符合KKT条件(设定一定的容错率)的alpha的优化
    在设定的迭代最大周期中保持alpha变量不变,才能退出循环
    """
    def fastSMO(self, C, toler = 0.001, maxIter = 50, kernel = ["linear"]):
        iterNum = 0
        self.C = C; self.toler = toler; self.kernel = kernel
        while (iterNum < maxIter) and (self.alphaPairChangedNum>0):
            self.alphaPairChangedNum = 0
            print("第%d次迭代"  %(iterNum+1))
            for AlphaindexI in range(self.sampleNum):
                if (self.AlphaIndexNotFitKKTconditon(AlphaindexI, toler)):
                    if(self.getUnbountAlphasSize() >= 1):
                        self.HeuristicAlphaProcess(AlphaindexI)
                    if (self.getUnbountAlphasSize() >= 2) and (self.isAlphaUpdate() == 0):
                        self.UnBoundAlphaProcess(AlphaindexI)
                    if self.isAlphaUpdate() == 0:
                        self.BoundAlphaProcess(AlphaindexI)
                    print("----------1 sample end")
            iterNum = self.updateIterNumByalphaPairChanged(iterNum)
            self.IsAlphaUpdate = 0;
        return self.b, self.alphasColumn
    
    """
    toler为容错限度,在toler范围内违反KKT条件是允许的
    """
    def AlphaIndexNotFitKKTconditon(self, index, toler):
        self.getPredictError(index)
        condition1 = (self.labelsColumn[index] * self.E[index] < -toler) and (self.alphasColumn[index] < self.C)
        condition2 = (self.labelsColumn[index] * self.E[index] > toler) and (self.alphasColumn[index] > 0)
        return condition1 or condition2
        
    def HeuristicAlphaProcess(self, AlphaindexI):
        print(">> Heuristic")
        self.getMaxStepAlphaIndex(AlphaindexI)
        self.process(AlphaindexI, self.MaxEiandIndex[1])

    def process(self, AlphaindexI, AlphaindexJ):
        ChangedNumOld = self.alphaPairChangedNum
        self.updateAlphaPairAndB(AlphaindexI, AlphaindexJ)
        self.updateAlphasArr(AlphaindexI, AlphaindexJ)
        self.IsAlphaUpdate = (ChangedNumOld != self.alphaPairChangedNum)
    
    def getUnbountAlphasSize(self):
        return np.sum(self.alphasNotBound)
    
    """
    这一步计算量较大
    """
    def getMaxStepAlphaIndex(self, indexI):
        for indexJ in range(self.sampleNum):
            if(self.alphasNotBound[indexJ] == 1):
                self.getPredictError(indexJ)
                self.updateMaxE(indexI, indexJ)
    
    def updateMaxE(self, indexI, indexJ):
        if abs(self.MaxEiandIndex[0]-self.E[indexI]) < abs(self.E[indexJ]-self.E[indexI]):
            self.MaxEiandIndex[0] = self.E[indexJ]
            self.MaxEiandIndex[1] = indexJ
    
    """
    计算量极大，但是一般在UNbound迭代步就能找到合适的indexJ。很少运行这一步
    """
    def BoundAlphaProcess(self, AlphaindexI):
        """
        迭代整一个Boundalpha 集合, 可以保证每个alpha值都会迭代到
        """
        print(">> bound")
        Bound = 1
        self.BoundOrNotProcess(Bound, AlphaindexI)
    
    def isAlphaUpdate(self):
        return self.IsAlphaUpdate

    def UnBoundAlphaProcess(self, AlphaindexI):
        print(">> unbound")
        Bound = 0
        self.BoundOrNotProcess(Bound, AlphaindexI)
    
    def BoundOrNotProcess(self, Bound, AlphaindexI):
        alphaIndexJ = int(random.uniform(0, self.sampleNum))
        boundindexSet, unboundindexSet = self.SeperateAlphaToBoundOrNot()
        if(Bound):
            for unuseful in boundindexSet:
                self.getPredictError(boundindexSet[alphaIndexJ % len(boundindexSet)])
                self.process(AlphaindexI, boundindexSet[alphaIndexJ % len(boundindexSet)])
                if self.isAlphaUpdate():
                    print(">> OK")
                    return
                alphaIndexJ = (alphaIndexJ + 1)
                
        else:
            for unuseful in unboundindexSet:
                self.process(AlphaindexI, unboundindexSet[alphaIndexJ % len(unboundindexSet)])
                if self.isAlphaUpdate():
                    print(">> OK")
                    return
                alphaIndexJ = (alphaIndexJ + 1)

    def SeperateAlphaToBoundOrNot(self):
        bound=[];unbound=[]
        for index in range(self.sampleNum):
            if(self.alphasNotBound[index] == 0):
                bound.append(index)
            else:
                unbound.append(index)
            #print("unbound=",unbound,'\n',self.alphasColumn[self.alphasNotBound==1])
            #print(self.alphasColumn)
        return bound, unbound

    def getPredictError(self, sampleindex):
         self.E[sampleindex] = self.predict(self.getSamplebyIndex(sampleindex))- float(self.labelsColumn[sampleindex])
   
    def predict(self, sampleRow):
#         y = wx + b
        if (self.kernel[0]=='linear'):
            fXi = float(self.Kernel(self.getW(), sampleRow, self.kernel)) + self.b
        else:
            fXi =  float(np.multiply(self.alphasColumn,self.labelsColumn).T * self.getKernelSUM(sampleRow)) + self.b
        return fXi
    
    """
    对于非线性核函数来说，这一步计算量是很大的。
    改进方法：kernel(x1,x2)仅与kernel参数和样本有关，所以可以提前算好，用查询就可以
    """
    def getKernelSUM(self, sampleRow):
        kernelSum = np.mat(np.zeros((self.sampleNum,1)))
        for index in range(self.sampleNum):
            kernelSum[index] = self.Kernel(self.samplesMat[index,:], sampleRow, self.kernel)
        return kernelSum
        
    def getW(self):
        # return [[0.8, -0.28]]
        wRow = np.multiply(self.alphasColumn,self.labelsColumn).T*self.samplesMat
        return wRow
    
    def getSamplebyIndex(self, index):
        sampleRow = self.samplesMat[index,:]
        return sampleRow
       
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
                self.prompt(i, j)
            else:
                print("\talpha_j变化太小  (%d %d)"%(i,j)); 
    
    def CopyOldAlpha(self, index):
        return self.alphasColumn[index].copy(); 

    def CalculateEta(self, i, j):
        self.eta = 2.0 * self.Cross(i, j) - self.Cross(i, i) - self.Cross(j, j)
        return self.eta

    def Cross(self, xRowIndex1, xRowIndex2):
        return self.Kernel(self.samplesMat[xRowIndex1,:], self.samplesMat[xRowIndex2,:], self.kernel)
        
    def Kernel(self, x1, x2, property):
        if(property[0] == 'linear'):
            return x1 * x2.T
        elif (property[0] == 'rbf'):
            omega = property[1]
            return np.exp(-np.sum(np.square(x1-x2))/(omega**2))

    def CalculateAlphaJUpandDown(self, i, j, C):
        if (self.labelsColumn[i] != self.labelsColumn[j]):
            L = max(0, self.alphasColumn[j] - self.alphasColumn[i])
            H = min(C, C + self.alphasColumn[j] - self.alphasColumn[i])
        else:
            L = max(0, self.alphasColumn[j] + self.alphasColumn[i] - C)
            H = min(C, self.alphasColumn[j] + self.alphasColumn[i])
        return H, L

    def updateAlphaJ(self, i, j):
        self.getPredictError(j)
        self.alphasColumn[j] -= self.labelsColumn[j]*(self.E[i] - self.E[j])/self.eta
        self.alphasColumn[j] = self.clipAlpha(self.alphasColumn[j], self.H, self.L)

    def updateAlphaI(self, i, j):
        self.alphasColumn[i] += self.labelsColumn[j]*self.labelsColumn[i]*(self.alphaJold - self.alphasColumn[j])
   
    def updateAlphasArr(self, i, j):
        if (0 < self.alphasColumn[i] < self.C):
            self.alphasNotBound[i]=1
        else:
            self.alphasNotBound[i]=0
        if (0 < self.alphasColumn[j] < self.C):
            self.alphasNotBound[j]=1
        else:
            self.alphasNotBound[j]=0
            
    def updateB(self, i, j):
        b1 = self.b - self.E[i] \
            - self.labelsColumn[i]*(self.alphasColumn[i]-self.alphaIold)*self.Cross(i, i) \
            - self.labelsColumn[j]*(self.alphasColumn[j]-self.alphaJold)*self.Cross(i, j)
        b2 = self.b - self.E[j] \
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
        print("\tAlpha优化次数:%d" %(self.alphaPairChangedNum))
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
    
    def test_hardSVM(self):
        samples2D=[[0,0],[4,0],[5,0]]; labels = [-1,1,1]
        smo = SMOSolver(samples2D, labels)
        b,alphasColumn = smo.fastSMO(C = 10000, toler = 0.001, maxIter = 40)
        w = smo.getW()
        if(b==[[-1]]) and (w[0,0]==0.5) and (w[0,1]==0):
            print("ture")
        else:
            print("false: w=",w,"b=",b)
        
        samples2D=[[0,0],[0,4]]; labels = [-1,1]
        smo = SMOSolver(samples2D, labels)
        b,alphasColumn = smo.fastSMO(C = 10000, toler = 0.001, maxIter = 40)
        w = smo.getW()
        if(b==[[-1]]) and (w[0,0]==0) and (w[0,1]==0.5):
            print("ture")
        else:
            print("false: w=",w,"b=",b)
            
    def test_SVMapplicaiton(self):
        samples2D, labels = my.loadDataSet('testDataSimple.txt')
        smo = SMOSolver(samples2D, labels)
        b,alphasColumn = smo.fastSMO(C = 10000, toler = 0.001, maxIter = 40)
        w = smo.getW()
        if(smo.test_EqualWithTolerant(b[0,0],-3.834,10*smo.toler) and \
            smo.test_EqualWithTolerant(w[0,0],0.814,smo.toler) and \
            smo.test_EqualWithTolerant(w[0,1],-0.272,smo.toler)) :
            print("ture")
        else:
            print("false: w=",w,"b=",b)
        
        smo.showResult()
    
    def test_RBFSVM(self):
        samples2D, labels = my.loadDataSet('testSetRBF.txt')
        smo = SMOSolver(samples2D, labels)
        b,alphasColumn = smo.fastSMO(C = 0.6, toler = 0.001, maxIter = 3, kernel=['rbf', 1])
        print("w=",smo.getW(),"b=",b)
        smo.showResult()
    
    def test(self):
        # SMOSolver().test_hardSVM()
        # SMOSolver().test_SVMapplicaiton()
        SMOSolver().test_RBFSVM()

        
if __name__ == '__main__':
    SMOSolver().test()

