import queue
import math
import copy
import numpy as np
import matplotlib.pyplot as plt


class clusterNode:
	def __init__(self, value, id=[],left=None, right=None, distance=-1,  count=-1, check = 0):
		'''
		value: 该节点的数值，合并节点时等于原来节点值的平均值
		id：节点的id，包含该节点下的所有单个元素
		left和right：合并得到该节点的两个子节点
		distance：两个子节点的距离
		count：该节点所包含的单个元素个数
		check：标识符，用于遍历时记录该节点是否被遍历过
		'''
		self.value = value
		self.id = id
		self.left = left
		self.right = right
		self.distance = distance
		self.count = count
		self.check = check

	def show(self):
		#显示节点相关属性
		print(self.value,' ',self.left.id if self.left!=None else None,' ',\
			self.right.id if self.right!=None else None,' ',self.distance,' ',self.count)

class hcluster:

	def distance(self,x,y):
		#计算两个节点的距离，可以换成别的距离
		return math.sqrt(pow((x.value-y.value),2))

	def minDist(self,dataset):
		#计算所有节点中距离最小的节点对
		mindist = 1000
		for i in range(len(dataset)-1):
			if dataset[i].check == 1:
				#略过合并过的节点
				continue
			for j in range(i+1,len(dataset)):
				if dataset[j].check == 1:
					continue
				dist = self.distance(dataset[i],dataset[j])
				if dist < mindist:
					mindist = dist
					x, y = i, j
		return mindist, x, y
		#返回最小距离、距离最小的两个节点的索引

	def fit(self,data):
		dataset = [clusterNode(value=item,id=[(chr(ord('a')+i))],count=1) for i,item in enumerate(data)]
		#将输入的数据元素转化成节点，并存入节点的列表
		length = len(dataset)
		Backup = copy.deepcopy(dataset)
		#备份数据
		while(True):
			mindist, x, y = self.minDist(dataset)
			dataset[x].check = 1
			dataset[y].check = 1
			tmpid = copy.deepcopy(dataset[x].id)
			tmpid.extend(dataset[y].id)
			dataset.append(clusterNode(value=(dataset[x].value+dataset[y].value)/2,id=tmpid,\
				left=dataset[x],right=dataset[y],distance=mindist,count=dataset[x].count+dataset[y].count))
			#生成新节点
			if len(tmpid) == length:
				#当新生成的节点已经包含所有元素时，退出循环，完成聚类
				break
		for item in dataset:
			item.show()
		return dataset

	def show(self,dataset,num):
		plt.figure(1)
		showqueue = queue.Queue()
		#存放节点信息的队列
		showqueue.put(dataset[len(dataset) - 1])
		#存入根节点
		showqueue.put(num)
		#存入根节点的中心横坐标
		while not showqueue.empty():
			index = showqueue.get()
			#当前绘制的节点
			i = showqueue.get()
			#当前绘制节点中心的横坐标
			left = i - (index.count)/2
			right = i + (index.count)/2
			if index.left != None:
				x = [left,right]
				y = [index.distance,index.distance]
				plt.plot(x,y)
				x = [left,left]
				y = [index.distance,index.left.distance]
				plt.plot(x,y)
				showqueue.put(index.left)
				showqueue.put(left)
			if index.right != None:
				x = [right,right]
				y = [index.distance,index.right.distance]
				plt.plot(x,y)
				showqueue.put(index.right)
				showqueue.put(right)
		plt.show()

def setData(num):
	#生成num个随机数据
	Data = list(np.random.randint(1,100,size=num))
	return Data

if __name__ == '__main__':
	num = 20
	dataset = setData(num)
	h = hcluster()
	resultset = h.fit(dataset)
	h.show(resultset,num)
