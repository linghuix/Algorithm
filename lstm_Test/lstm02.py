# coding=gbk
# lstm输入一串连续质数预估下一个质数。
# 小测试，生成100以内质数，循环拿出50个质数序列作x，第51个质数作y，
# 拿出10个样本参与训练1w次，
# 均方误差由0.17973最终达到了1.05172e-06，几乎完全正确：

import numpy as np


from h.lstm import LstmParam, LstmNetwork

class ToyLossLayer:
    """
    Computes square loss with first element of hidden layer array.
    """
    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2
    
    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff

class Primes:
    def __init__(self):
        self.primes = list()
        for i in range(2, 500):
            is_prime = True
            for j in range(2, i-1):
                if i % j == 0:
                    is_prime = False
            if is_prime:
                self.primes.append(i)
                self.primes_count = len(self.primes)
        print ("prime_list= %f", self.primes)
    def get_sample(self, x_dim, y_dim, index):
        result = np.zeros((x_dim+y_dim))
        for i in range(index, index + x_dim + y_dim):
            result[i-index] = self.primes[i%self.primes_count]/1000.0
        return result

def example_0():
    # size of net。100 nodes and 50 input
    mem_cell_ct = 1
    x_dim = 50
    # concat_len = x_dim + mem_cell_ct
    lstm_param = LstmParam(mem_cell_ct, x_dim)
    lstm_net = LstmNetwork(lstm_param)
    
    # get x_list and y_list data
    primes = Primes()
    x_list = []
    y_list = []
    for i in range(0, 10):
        sample = primes.get_sample(x_dim, 1, i)
        x = sample[0:x_dim]
        y = sample[x_dim:x_dim+1].tolist()[0]
        x_list.append(x)
        y_list.append(y)
    print ("x_list= ", x_list)
    print ("y_list= ", y_list)
    
    # repeat n times
    for cur_iter in range(10000):
                #print("cur_iter number = ",cur_iter)
        if cur_iter % 1000 == 0:
            print ("y_list= ", y_list)
            # print ("x_list= ", x_list)
        for ind in range(len(y_list)):
            # add x data to the lstm_net and calculate the parameters of len(y_list)'s netnode
            lstm_net.x_list_add(x_list[ind])
    
            if cur_iter % 1000 == 0 and ind == 8:
                # print ("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.h(0)))
                # h of each node is 1*100 dimension
                print (ind, lstm_net.lstm_node_list[ind].state.h)
                    
        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        if cur_iter % 1000 == 0:
            print ("loss: %.30f" % loss)
        lstm_param.apply_diff(lr=0.01)
        lstm_net.x_list_clear()


if __name__ == "__main__":
    example_0()
# 质数列表全都除以100，这个代码训练数据必须是小于1数值。