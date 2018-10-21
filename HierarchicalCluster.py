import math
import copy
import numpy as np
import matplotlib.pyplot as plt


class clusterNode:
	def __init__(self, value, id=[],left=None, right=None, distance=-1,  count=-1, check = 0):
		self.value = value
		self.id = id
		self.left = left
		self.right = right
		self.distance = distance
		self.count = count
		self.check = check

	def show(self):
		print(self.value,' ',self.left.id if self.left!=None else None,' ',\
			self.right.id if self.right!=None else None,' ',self.distance,' ',self.count)

class hcluster:

	def distance(self,x,y):
		return math.sqrt(pow((x.value-y.value),2))

	def minDist(self,dataset):
		mindist = 1000
		for i in range(len(dataset)-1):
			if dataset[i].check == 1:
				continue
			for j in range(i+1,len(dataset)):
				if dataset[j].check == 1:
					continue
				dist = self.distance(dataset[i],dataset[j])
				if dist < mindist:
					mindist = dist
					x, y = i, j
		return mindist, x, y

	def fit(self,data):
		dataset = [clusterNode(value=item,id=[(chr(ord('a')+i))],count=1) for i,item in enumerate(data)]
		length = len(dataset)
		Backup = copy.deepcopy(dataset)
		while(True):
			mindist, x, y = self.minDist(dataset)
			dataset[x].check = 1
			dataset[y].check = 1

			tmpid = copy.deepcopy(dataset[x].id)
			tmpid.extend(dataset[y].id)
			dataset.append(clusterNode(value=(dataset[x].value+dataset[y].value)/2,id=tmpid,\
				left=dataset[x],right=dataset[y],distance=mindist,count=dataset[x].count+dataset[y].count))
			if len(tmpid) == length:
				break
		return dataset

	def show(self,dataset):
		for item in dataset:
			item.show()
	# def makeplt(self,a,dataset,index,i):
	# 	if index.left == None and index.right == None:
	# 		return a
	# 	else:
	# 		if index.left != None:
	# 			left = i - (index.count) / 2
	# 			right = i + (index.count) / 2
	# 			x = [left,right]
	# 			y = [index.distance,index.distance]
	# 			a.plot(x,y)
	# 			i = left
	# 			index = index.left
	# 			a = self.makeplt(a,dataset,index,i)
	# 		if index.right != None:
	# 			left = i - (index.count) / 2
	# 			right = i + (index.count) / 2
	# 			x = [left,right]
	# 			y = [index.distance,index.distance]
	# 			a.plot(x,y)
	# 			i = right
	# 			index = index.right
	# 			a = self.makeplt(a,dataset,index,i)

	# def show(self,dataset):
	# 	index = dataset[len(dataset) - 1]
	# 	a = plt.figure()
	# 	i = 10
	# 	self.makeplt(plt,dataset,index,i)
	# 	a.show()

def setData(num):
	Data = list(np.random.randint(1,100,size=10))
	return Data

if __name__ == '__main__':
	dataset = setData(10)
	h = hcluster()
	resultset = h.fit(dataset)
	h.show(resultset)