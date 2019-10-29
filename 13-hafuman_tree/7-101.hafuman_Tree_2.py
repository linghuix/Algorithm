# -*- coding: utf-8 -*-
"""
 /*哈希数据结构
 * 对查找，添加比较方便
 * 
 * 对于搜索，查找最大值，最小值，排序并不是很方便，但是可以实现
 * 搜索，查找最大值需要扫描整个保存的数据
 * 排序需要，传入对应的空间，存储关键词和对应的值，根据对应的值进行排序。
 *
 * */
"""
# 树节点类构建
class TreeNode(object):
  def __init__(self, data):
    self.val = data[0]
    self.priority = data[1]
    self.leftChild = None
    self.rightChild = None
    self.code = ""
    
# 创建树节点队列函数
def creatnodeQ(codes):
  q = []
  for code in codes:
    q.append(TreeNode(code))
  return q
  
# 为队列添加节点元素，并保证优先度从大到小排列
def addQ(queue, nodeNew):
  if len(queue) == 0:
    return [nodeNew]
  for i in range(len(queue)):
    if queue[i].priority >= nodeNew.priority:
      return queue[:i] + [nodeNew] + queue[i:]
  return queue + [nodeNew]
  
# 节点队列类定义
class nodeQeuen(object):
 
  def __init__(self, code):
    self.que = creatnodeQ(code)
    self.size = len(self.que)
 
  def addNode(self,node):
    self.que = addQ(self.que, node)
    self.size += 1
 
  def popNode(self):
    self.size -= 1
    return self.que.pop(0)
    
# 各个字符在字符串中出现的次数，即计算优先度
def freChar(string):
  d ={}
  for c in string:
    if not c in d:
      d[c] = 1
    else:
      d[c] += 1
  return sorted(d.items(),key=lambda x:x[1])
  
# 创建哈夫曼树
def creatHuffmanTree(nodeQ):
  while nodeQ.size != 1:
    node1 = nodeQ.popNode()
    node2 = nodeQ.popNode()
    r = TreeNode([None, node1.priority+node2.priority])
    r.leftChild = node1
    r.rightChild = node2
    nodeQ.addNode(r)
  return nodeQ.popNode()
 
codeDic1 = {}
codeDic2 = {}

# 由哈夫曼树得到哈夫曼编码表
def HuffmanCodeDic(head, x):
  global codeDic, codeList
  if head:
    HuffmanCodeDic(head.leftChild, x+'0')
    head.code += x
    if head.val:
      codeDic2[head.code] = head.val
      codeDic1[head.val] = head.code
    HuffmanCodeDic(head.rightChild, x+'1')
    
# 字符串编码
def TransEncode(string):
  global codeDic1
  transcode = ""
  for c in string:
    transcode += codeDic1[c]
  return transcode
  
# 字符串解码
def TransDecode(StringCode):
  global codeDic2
  code = ""
  ans = ""
  for ch in StringCode:
    code += ch
    if code in codeDic2:
      ans += codeDic2[code]
      code = ""
  return ans

def WriteBinString(StringCode,path):
	
	import struct

	## write BIN data
	savedBinFile = open(path, "wb"); # open a file, if not exist, create it

	#不足8个的部分
	surplus = len(StringCode)-len(StringCode)//8*8
	index = surplus										
	code = struct.pack("B", 8-index)	#看做数字或者char，打包成1个字节，这样才能写入二进制文件中
	savedBinFile.write(code)
	code = struct.pack("B", int(StringCode[0:index],2))	#二进制字符串，先化为十进制数，再进行字节化
	savedBinFile.write(code)

	#剩下的字符串都是8个的
	while(index+8 <= len(StringCode)):	
		code = struct.pack("B", int(StringCode[index:index+8],2))
		savedBinFile.write(code);
		index = index+8

	savedBinFile.close()


def ReadBinString(path):
	
	import struct
	BinFile = open(path, "rb");

	# 处理头部
	head_index = BinFile.read(1)
	head_index = int(struct.unpack("B",head_index)[0])

	head_str = BinFile.read(1)
	head_str = struct.unpack("B",head_str)
	read_bin_str = bin(head_str[0])[2:].rjust(8, "0")[head_index:]	# 十进制数化为二进制字符串
	#print(head_str,read_bin_str)

	# 处理正文
	while(True):
		by = BinFile.read(1)
		if not by: break
		#print('ReadBinString: bytes=',by)
		num = struct.unpack("B",by)
		bin_str_part = bin(num[0])[2:].rjust(8, "0")
		#print(bin(code[0]),bin_str_part)
		read_bin_str = read_bin_str+bin_str_part

	return read_bin_str

def SaveDict(filename, d):

	import pickle
	
	file= open(filename,'wb')
	pickle.dump(d, file, -1)
	

# ### 举例

# 打开需要编码的文件
f = open(r"/mnt/Documents/100-语言/Algorithm/new.txt")
string = f.read()


# 打印编码集
t = nodeQeuen(freChar(string))
tree = creatHuffmanTree(t)
HuffmanCodeDic(tree, '')
print("打印编码集")
print("codeDic1:",codeDic1,"\ncodeDic2:",codeDic2)

# 进行编码
bin_str = TransEncode(string)
print("\n\n编码结果",bin_str,'\n\n')

## write BIN data
WriteBinString(bin_str,r"/mnt/Documents/100-语言/Algorithm/Huffman_Encode.bin")

## reading and encode the BIN data
read_bin_str = ReadBinString(r"/mnt/Documents/100-语言/Algorithm/Huffman_Encode.bin");


#print("READ:",read_bin_str)
#print("\n\n编码结果",BIN)

print("compare:",read_bin_str == bin_str)

print("--------------------------\n",TransDecode(read_bin_str))
SaveDict(r"/mnt/Documents/100-语言/Algorithm/Huffman_dict.txt",codeDic2)


