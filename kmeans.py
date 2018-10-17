import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def setData():
	#随机生成100个二位数据
	x = np.random.rand(100)
	y = np.random.rand(100)
	loc = list(zip(x,y))
	dots = pd.DataFrame(loc,columns=['x','y'])
	dots['tag'] = -1
	#每个点所属的中心，初值为-1
	return dots

def show(dataset,centroid,k):
	#生成结果图像
	fig = plt.figure(k)
	cmark = ['b','g','r']
	for i in range(len(dataset)):
		plt.scatter(dataset['x'][i],dataset['y'][i],color=cmark[dataset['tag'][i]])
	plt.scatter(centroid['x'],centroid['y'],color='k')
	fig.savefig('result'+str(k)+'.png')
	#保存结果

def length(x,y,cx,cy):
	#计算距离，为了计算方便没有开方
	return pow(x-cx,2) + pow(y-cy,2)

def calcenter(dataset):
	#计算中心
	x = [0,0,0]
	y = [0,0,0]
	num = [0,0,0]
	for index, row in dataset.iterrows():
		i = int(row['tag'])
		x[i] += row['x']
		y[i] += row['y']
		num[i] += 1
	for i in range(3):
		x[i] = x[i] / num[i]
		y[i] = y[i] / num[i]
	centroid = pd.DataFrame({'x':x,'y':y})
	return centroid

def judge(old,new):
	#判断新、旧的中心是否有变动
	for index, row in old.iterrows():
		for i in ['x','y']:
			if row[i] != new[i][index]:
				return 0
	return 1


def kmeans(dataset,k):
	#k-means算法，k为中心个数，返回中心点坐标，并保存每次求得图像
	centroid = pd.DataFrame(list(zip(np.random.rand(k),np.random.rand(k))),columns=['x','y'])
	print(centroid)
	#随机初始化中心
	old_centroid = pd.DataFrame({'x':[0,0,0],'y':[0,0,0]})
	#初始化旧的中心
	len = [0,0,0]
	#点到各中心的距离

	flag = 1
	time = 0
	show(dataset,centroid,time)
	#保存初始值
	while(time<20 and judge(old_centroid,centroid)==0):
		time += 1
		old_centroid = centroid
		for index, row in dataset.iterrows():
			len[0] = length(row['x'],row['y'],centroid['x'][0],centroid['y'][0])
			len[1] = length(row['x'],row['y'],centroid['x'][1],centroid['y'][1])
			len[2] = length(row['x'],row['y'],centroid['x'][2],centroid['y'][2])
			tmp = len.index(min(len))
			if(dataset['tag'][index] != tmp):
				dataset['tag'][index] = tmp
				#报警告：A value is trying to be set on a copy of a slice from a DataFrame
		centroid = calcenter(dataset)
		show(dataset,centroid,time)
		#保存每次计算的结果
	print(time)
	return centroid

def main():
	#主程序，显示中心
	dataset = setData();
	print(dataset)
	print(kmeans(dataset,3))

if __name__=='__main__':
	main()