"""*哈希数据结构
 * 对查找，添加比较方便
 * 
 * 对于搜索，查找最大值，最小值，排序并不是很方便，但是可以实现
 * 搜索，查找最大值需要扫描整个保存的数据
 * 排序需要，传入对应的空间，存储关键词和对应的值，根据对应的值进行排序。
 *
 * */"""
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


# ### 举例

import binascii
# 打开需要编码的文件
f = open(r"C:\Users\pc\Downloads\new.txt")
string = f.read()
# print(string)
# string = "AAGGDCCCDDDGFBBBFFGGDDDDGGGEFFDDCCCCDDFGAAA"
t = nodeQeuen(freChar(string))
tree = creatHuffmanTree(t)
HuffmanCodeDic(tree, '')

# 打印编码集
print(codeDic1)
print(codeDic2)

# 进行编码
bin_str = TransEncode(string)
print(bin_str)

#	以某种编码方式进行编码，转化为字节
bin_data = bin_str.encode()

print(len(bin_data))
savedBinFile = open(r"D:\100-语言\Algorithm\13-hafuman_tree\Encode.bin", "wb"); # open a file, if not exist, create it
savedBinFile.write(bin_data);
savedBinFile.close();


BinFile = open(r"Encode.bin", "rb");
# 读取一个字节，2进制形式的
a = BinFile.read(1)

# 转化为16进制形式的字符串
# c = binascii.b2a_hex(a)

# 获得16进制形式的字符串
s = str(a)[4:-1]

# 根据十六进制字符串获得二进制串。 一个十六进制对应4个二进制，补足零
string = hex2bin(s,dict_Me)


print(string == aa)

savedFile = open(r"C:\Users\pc\Downloads\Decode.txt", "w");
savedFile.write(aa)

#>>> c=struct.pack("B", int("11010101",2))
#>>> bin(struct.unpack("B", c)[0])
# '0b11010101'

