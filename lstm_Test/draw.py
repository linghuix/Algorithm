# coding=gbk
'''>x x轴
> y y轴
> s   圆点面积
> c   颜色
> marker  圆点形状
> alpha   圆点透明度                #其他图也类似这种配置</pre>'''
import numpy as np
import matplotlib.pyplot as plt

# 散点图
N=50
# height=np.random.randint(150,180,20)
# weight=np.random.randint(80,150,20)
x=np.random.randn(N)
y=np.random.randn(N)
plt.scatter(x,y, s=50,c='r',marker='o',alpha=0.5)
plt.show()

# 折线图
x=np.linspace(-10,10,100) #将-10到10等区间分成100份
y=x**2+x**3+x**7
plt.plot(x,y)
plt.show()
'''
# 条形图
N=5
y=[20,10,30,25,15]
y1=np.random.randint(10,50,5)
x=np.random.randint(10,1000,N)
index=np.arange(N)
print(index)
plt.bar(index,y,color='red',width=0.3)
plt.bar(left=index+0.3,height=y1,color='black',width=0.3)
plt.show()

# orientation设置横向条形图
N=5
y=[20,10,30,25,15]
y1=np.random.randint(10,50,5)
x=np.random.randint(10,1000,N)
index=np.arange(N)
# plt.bar(left=index,height=y,color='red',width=0.3)
# plt.bar(left=index+0.3,height=y1,color='black',width=0.3)
#plt.barh() 加了h就是横向的条形图，不用设置orientation
plt.bar(left=0,bottom=index,width=y,color='red',height=0.5,orientation='horizontal')
plt.show()'''

# .直方图
m1=100
sigma=20
x=m1+sigma*np.random.randn(2000)
plt.hist(x,bins=50,color="green",normed=True)
plt.show()

#双变量的直方图
#颜色越深频率越高
#研究双变量的联合分布
x=np.random.rand(1000)+2
y=np.random.rand(1000)+3
plt.hist2d(x,y,bins=40)
plt.show()

# 饼状图
# 设置x,y轴比例为1：1，从而达到一个正的圆</pre>
# abels标签参数,x是对应的数据列表,
# autopct显示每一个区域占的比例,
# explode突出显示某一块,
# shadow阴影</pre>
labes=['A','B','C','D']
fracs=[15,30,45,10]
explode=[0,0.1,0.05,0]
#设置x,y轴比例为1：1，从而达到一个正的圆
plt.axes(aspect=1)
#labels标签参数,x是对应的数据列表,autopct显示每一个区域占的比例,explode突出显示某一块,shadow阴影
plt.pie(x=fracs,labels=labes,autopct="%.0f%%",explode=explode,shadow=True)
plt.show()

# 8.箱型图 
data=np.random.normal(loc=0,scale=1,size=1000)
#sym 点的形状，whis虚线的长度
plt.boxplot(data,sym="o",whis=1.5)
plt.show()



