# -*- coding: utf-8 -*-


# 字符串解码
def TransDecode(StringCode,codeDic2):

  code = ""
  ans = ""
  for ch in StringCode:
    code += ch
    if code in codeDic2:
      ans += codeDic2[code]
      code = ""
  return ans

def ReadDict(filename):

	import pickle
	
	file= open(filename,'rb')
	codeDic=pickle.load(file)
	return codeDic

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
	

# ### 举例
import pickle
read_bin_str = ReadBinString(r"/mnt/Documents/100-语言/Algorithm/Huffman_Encode.bin");
codeDic = ReadDict(r"/mnt/Documents/100-语言/Algorithm/Huffman_dict.txt") 
print("-----------------------------------\n",TransDecode(read_bin_str,codeDic))


