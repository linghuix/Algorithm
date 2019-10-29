# coding=gbk

"""
输入x 50维，输出y 1维。由于lstm的特性，这里设置 h 为100维,即记录的时间跨度为100个单位
输出的向量仅将第一个数字用来预测y,计算误差也只是用h(0)

数据输入的流程。以四个数据(x = 1*50dim  y = 1*1dim)为一组看做一个流，
将每个时刻的误差与参数的导数累加起来，然后进行最速梯度下降法更新参数。

RNN作为重要的是，把序列看做是一组参数，各个时刻的导数相互有影响，并且更新参数的时候是一组加起来更新的
(因为要计算一个的导数，必须计算其他时刻的导数，所以更新的时候就把有关联的导数一起计算了，一步更新到位)
x(n)与x(n-1)有关，类似于VARx，进行拟合(x,y)
"""


import numpy as np

from lstm import LstmParam, LstmNetwork

class ToyLossLayer:
   
    # Computes square loss with first element of hidden layer array of one lstm node.

    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff

def example_0():
    # learns to repeat simple sequence from random inputs
    np.random.seed(0)

    # parameters for input data dimension and lstm cell count 
    mem_cell_ct = 100
    x_dim = 50
    concat_len = x_dim + mem_cell_ct
    lstm_param = LstmParam(mem_cell_ct, x_dim) 
    lstm_net = LstmNetwork(lstm_param)
    
    # predict number
    y_list = [-0.5, 0.2, 0.1, -0.4]
    input_val_arr = [np.random.random(x_dim) for _ in y_list] # 一个list，包含随机生成的4个 array(50)
    #  print(input_val_arr)
    
    # 四个数据为一组，循环100遍
    for cur_iter in range(100):
        print ("cur_iter : ", cur_iter)
        
        # 四个数据为一组，对应y值。进行参数更新
        for ind in range(len(y_list)):
            # 前向传播
            lstm_net.x_list_add(input_val_arr[ind])
            print ("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.h[0]),lstm_net.lstm_node_list[ind].state.h.shape)
            print(lstm_net.lstm_node_list[ind].state.h)

        # 反向传播
        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        # print ("loss: "), loss
        print ("loss: %f" % loss)
        
        # update the parameters
        lstm_param.apply_diff(lr=0.1)
        lstm_net.x_list_clear()


if __name__ == "__main__":
    example_0()
