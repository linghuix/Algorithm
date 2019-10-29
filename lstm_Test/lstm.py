# coding=gbk

#import numpy as np
#a = np.array([1,2,3])
#print(a)

# 每训练1000个样本输出总误差信息，运行时看收敛过程。
# LSTM最简单实现，没有考虑偏置变量，只有两个神经元。

import numpy as np

# 声明sigmoid函数
def sigmoid(x): 
    return 1. / (1 + np.exp(-x))

# create uniform random array values in [a,b) and shape args
# 生成随机矩阵，取值范围[a,b)，shape用args指定。
def rand_arr(a, b, *args): 
    np.random.seed(0)
    return np.random.rand(*args) * (b - a) + a

# LstmParam类传递参数，

'''
concat_len是mem_cell_ct与x_dim长度和，
wg是输入节点权重矩阵，wi是输入门权重矩阵，
wf是忘记门权重矩阵，wo是输出门权重矩阵，
bg、bi、bf、bo分别是输入节点、输入门、忘记门、输出门偏置，
wg_diff、wi_diff、wf_diff、wo_diff分别是输入节点、输入门、忘记门、输出门权重损失
bg_diff、bi_diff、bf_diff、bo_diff分别是输入节点、输入门、忘记门、输出门偏置损失
初始化按照矩阵维度初始化，损失矩阵归零。
'''

class LstmParam:
    
    # initing the parameters. call  rand_arr(a, b, *args)
    # mem_cell_ct是lstm神经元数目
    # x_dim是输入数据维度
    def __init__(self, mem_cell_ct, x_dim):
        self.mem_cell_ct = mem_cell_ct
        self.x_dim = x_dim
        concat_len = x_dim + mem_cell_ct
        # weight matrices
        self.wg = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wi = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len) 
        self.wf = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wo = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        # bias terms
        self.bg = rand_arr(-0.1, 0.1, mem_cell_ct) 
        self.bi = rand_arr(-0.1, 0.1, mem_cell_ct) 
        self.bf = rand_arr(-0.1, 0.1, mem_cell_ct) 
        self.bo = rand_arr(-0.1, 0.1, mem_cell_ct) 
        # diffs (derivative of loss function w.r.t. all parameters)
        self.wg_diff = np.zeros((mem_cell_ct, concat_len)) 
        self.wi_diff = np.zeros((mem_cell_ct, concat_len)) 
        self.wf_diff = np.zeros((mem_cell_ct, concat_len)) 
        self.wo_diff = np.zeros((mem_cell_ct, concat_len)) 
        self.bg_diff = np.zeros(mem_cell_ct) 
        self.bi_diff = np.zeros(mem_cell_ct) 
        self.bf_diff = np.zeros(mem_cell_ct) 
        self.bo_diff = np.zeros(mem_cell_ct) 

    # 定义权重更新过程，先减损失，再把损失矩阵归零。
    # self 相当于调用某个类的实例
    def apply_diff(self, lr = 1):
        self.wg -= lr * self.wg_diff
        self.wi -= lr * self.wi_diff
        self.wf -= lr * self.wf_diff
        self.wo -= lr * self.wo_diff
        self.bg -= lr * self.bg_diff
        self.bi -= lr * self.bi_diff
        self.bf -= lr * self.bf_diff
        self.bo -= lr * self.bo_diff
        # reset diffs to zero
        self.wg_diff = np.zeros_like(self.wg)
        self.wi_diff = np.zeros_like(self.wi) 
        self.wf_diff = np.zeros_like(self.wf) 
        self.wo_diff = np.zeros_like(self.wo) 
        self.bg_diff = np.zeros_like(self.bg)
        self.bi_diff = np.zeros_like(self.bi) 
        self.bf_diff = np.zeros_like(self.bf) 
        self.bo_diff = np.zeros_like(self.bo) 

'''LstmState存储LSTM神经元状态，
g、i、f、o、s、h，s ，h是隐藏层神经元输出矩阵。'''
class LstmState:
    def __init__(self, mem_cell_ct, x_dim):
        self.g = np.zeros(mem_cell_ct)
        self.i = np.zeros(mem_cell_ct)
        self.f = np.zeros(mem_cell_ct)
        self.o = np.zeros(mem_cell_ct)
        self.s = np.zeros(mem_cell_ct)
        self.h = np.zeros(mem_cell_ct)
        self.bottom_diff_h = np.zeros_like(self.h)
        self.bottom_diff_s = np.zeros_like(self.s)
        self.bottom_diff_x = np.zeros(x_dim)

'''LstmNode对应样本输入，
x是输入样本x，
xc是用hstack把x和递归输入节点拼接矩阵
（hstack是横拼矩阵，vstack是纵拼矩阵）。
'''    
class LstmNode:
    def __init__(self, lstm_param, lstm_state):
        # store reference to parameters and to activations
        self.state = lstm_state
        self.param = lstm_param
        # non-recurrent input to node
        self.x = None
        # non-recurrent input concatenated with recurrent input
        self.xc = None
    
    ''' bottom和top是两个方向，输入样本从底部输入，反向传导从顶部向底部传导，
    bottom_data_is是输入样本过程，把x和先前输入拼接成矩阵，
        用公式wx+b分别计算g、i、f、o值，激活函数tanh和sigmoid。
        每个时序神经网络有四个神经网络层(激活函数)，
        最左边忘记门，直接生效到记忆C，
        第二个输入门，依赖输入样本数据，按照一定“比例”影响记忆C，
    “比例”通过第三个层(tanh)实现，取值范围是[-1,1]可以正向影响也可以负向影响，
        最后一个输出门，每一时序产生输出既依赖输入样本x和上一时序输出，还依赖记忆C，
        设计模仿生物神经元记忆功能。'''
        
    def bottom_data_is(self, x, s_prev = None, h_prev = None):
        # if this is the first lstm node in the network
        if [s_prev == None]: s_prev = np.zeros_like(self.state.s)
        if [h_prev == None]: h_prev = np.zeros_like(self.state.h)
        # save data for use in backprop
        self.s_prev = s_prev
        self.h_prev = h_prev

        # concatenate x(t) and h(t-1)
        xc = np.hstack((x,  h_prev))
        self.state.g = np.tanh(np.dot(self.param.wg, xc) + self.param.bg)
        self.state.i = sigmoid(np.dot(self.param.wi, xc) + self.param.bi)
        self.state.f = sigmoid(np.dot(self.param.wf, xc) + self.param.bf)
        self.state.o = sigmoid(np.dot(self.param.wo, xc) + self.param.bo)
        self.state.s = self.state.g * self.state.i + s_prev * self.state.f
        self.state.h = self.state.s * self.state.o
        self.x = x
        self.xc = xc
        # print(self.state.h)

    # L(t) = l(t) + L(t+1)，
    # dL(t)/dh(t) = dl(t)/dh(t) + dL(t+1)/dh(t)，
    # 用下一时序导数得出当前时序导数，规律推导，计算T时刻导数往前推，
    # 在T时刻，dL(T)/dh(T) = dl(T)/dh(T)。
	# top_diff_s 是该层之上的误差与s的导数。初始值就是0
	# top_diff_h 是该层之上的误差与h的导数。初始值就是2 * (h[0] - y)
	# 输出：bottom_diff  该层的误差与s，h的导数
    def top_diff_is(self, top_diff_h, top_diff_s):
        # notice that top_diff_s is carried along the constant error carousel
        ds = self.state.o * top_diff_h + top_diff_s
        do = self.state.s * top_diff_h
        di = self.state.g * ds
        dg = self.state.i * ds
        df = self.s_prev * ds

        # diffs w.r.t. vector inside sigma / tanh function
        di_input = (1. - self.state.i) * self.state.i * di 
        df_input = (1. - self.state.f) * self.state.f * df 
        do_input = (1. - self.state.o) * self.state.o * do 
        dg_input = (1. - self.state.g ** 2) * dg

        # diffs w.r.t. inputs  计算对每个需要训练的参数的导数
        self.param.wi_diff += np.outer(di_input, self.xc)
        self.param.wf_diff += np.outer(df_input, self.xc)
        self.param.wo_diff += np.outer(do_input, self.xc)
        self.param.wg_diff += np.outer(dg_input, self.xc)
        self.param.bi_diff += di_input
        self.param.bf_diff += df_input       
        self.param.bo_diff += do_input
        self.param.bg_diff += dg_input   
        # print('self.param.wi_diff = ',self.param.wi_diff.shape)		

        # compute bottom diff
        # xc is a vector ,+ means add the each elments of vector . xc include wi,wf,wo,wg. so need add dwi,dwf,dwo,dwg all
        dxc = np.zeros_like(self.xc)
        dxc += np.dot(self.param.wi.T, di_input)
        dxc += np.dot(self.param.wf.T, df_input)
        print('dxc_1.ndim=',dxc.shape)
        dxc += np.dot(self.param.wo.T, do_input)
        dxc += np.dot(self.param.wg.T, dg_input)
        # print('dxc_2.ndim=',dxc.shape)

        # save bottom diffs. xc = [x(t),h(t-1)]
        self.state.bottom_diff_s = ds * self.state.f
        self.state.bottom_diff_x = dxc[:self.param.x_dim]
        self.state.bottom_diff_h = dxc[self.param.x_dim:]

class LstmNetwork():
    def __init__(self, lstm_param):
        self.lstm_param = lstm_param
        self.lstm_node_list = []
        # input sequence
        self.x_list = []
    
    # backprop
    def y_list_is(self, y_list, loss_layer):
        """
        Updates diffs by setting target sequence 
        with corresponding loss layer. 
        Will *NOT* update parameters.  To update parameters,
        call self.lstm_param.apply_diff()
        """
        
        # ensure ...
        assert len(y_list) == len(self.x_list)
        
        # get the final node
        idx = len(self.x_list) - 1
        
        # first node only gets diffs from label ...
        # h is the output of lstmNode
        loss = loss_layer.loss(self.lstm_node_list[idx].state.h, y_list[idx])
        
        # 计算反向传播最开始的diff_h and diff_s,代码在LSTM_main内定义
        diff_h = loss_layer.bottom_diff(self.lstm_node_list[idx].state.h, y_list[idx])
        
        # here s is not affecting loss due to h(t+1), hence we set equal to zero
        diff_s = np.zeros(self.lstm_param.mem_cell_ct)
        self.lstm_node_list[idx].top_diff_is(diff_h, diff_s)
                #print(' '*idx,'backprop' ,idx,':')
        idx -= 1

        ### ... following nodes also get diffs from next nodes, hence we add diffs to diff_h
        ### we also propagate error along constant error carousel using diff_s
        while idx >= 0:
            # add all the loss (h(0)-y)
            loss += loss_layer.loss(self.lstm_node_list[idx].state.h, y_list[idx])
            diff_h = loss_layer.bottom_diff(self.lstm_node_list[idx].state.h, y_list[idx])
            
            # print('diff_h1 = ',diff_h.shape,diff_h)
            
            diff_h += self.lstm_node_list[idx + 1].state.bottom_diff_h
            
            # print('diff_h2 = ',diff_h.shape,diff_h)
            
            diff_s = self.lstm_node_list[idx + 1].state.bottom_diff_s
            self.lstm_node_list[idx].top_diff_is(diff_h, diff_s)
            # print(' '*idx,'backprop' ,idx,':')
            idx -= 1 

        return loss

    def x_list_clear(self):
        self.x_list = []
    
    # 添加训练样本，输入x数据. foreprop
    def x_list_add(self, x):
        self.x_list.append(x)
        if len(self.x_list) > len(self.lstm_node_list):
            # need to add new lstm node, create new state mem。 
            # the number of elements of lstm_node_list need to be the same as x_list's
            lstm_state = LstmState(self.lstm_param.mem_cell_ct, self.lstm_param.x_dim) # set lstm_state zero

            # create the new node whose param is the same as network
            self.lstm_node_list.append(LstmNode(self.lstm_param, lstm_state))


        # get index of most recent x input
        idx = len(self.x_list) - 1
                #print(' '*idx,'foreprop' ,idx,':')
        if idx == 0:
            # no recurrent inputs yet
            self.lstm_node_list[idx].bottom_data_is(x)
        else:
            s_prev = self.lstm_node_list[idx - 1].state.s
            h_prev = self.lstm_node_list[idx - 1].state.h
            # calculate the parameters
            self.lstm_node_list[idx].bottom_data_is(x, s_prev, h_prev) 
   

   
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
    mem_cell_ct = 1
    x_dim = 50
    concat_len = x_dim + mem_cell_ct
    lstm_param = LstmParam(mem_cell_ct, x_dim) 
    lstm_net = LstmNetwork(lstm_param)
    # predict number
    y_list = [-0.5,0.2,0.1, -0.4]
    input_val_arr = [np.random.random(x_dim) for _ in y_list] # input_val_arr get [[]1*50,[]1*50,[]1*50]1*4

    for cur_iter in range(100):
        print ("cur_iter : "), cur_iter
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])
            print ("y_pred[%d] : %f" %(ind, lstm_net.lstm_node_list[ind].state.h[0]), 'dim=',lstm_net.lstm_node_list[ind].state.h.shape)

        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        #print ("loss: "), loss
        print ("loss: %f" % loss)
        lstm_param.apply_diff(lr=0.1)
        lstm_net.x_list_clear()

if __name__ == "__main__":
    example_0()